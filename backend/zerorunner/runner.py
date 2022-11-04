# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

import copy
import os
import sys
import time
import traceback
import uuid
from datetime import datetime
from typing import List, Dict, Text, Any, Union
from loguru import logger
from zerorunner import exceptions
from zerorunner import utils
from zerorunner.client import HttpSession
from zerorunner.exceptions import ValidationFailure, ParamsError
from zerorunner.ext.db import DB
from zerorunner.ext.uploader import prepare_upload_step
from zerorunner.loader import load_script_content, load_module_functions
from zerorunner.models import (
    TConfig,
    TStep,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseTime,
    TestCaseInOut,
    TestCase,
    Hooks, FunctionsMapping, TStepController, Headers, TStepTypeEnum
)
from zerorunner.parser import parse_variables_mapping, parse_data, build_url, parse_parameters
from zerorunner.response import ResponseObject
from zerorunner.utils import merge_variables


class ZeroRunner(object):
    config: TConfig
    teststeps: List[Any]

    success: bool = False  # indicate testcase execution result
    message: Text = ""  # 错误信息或备注等信息记录
    __teststeps: List[Any]
    extracted_variables: VariablesMapping = {}
    __case_id: Text = ""
    __export: List[Text] = []
    __step_datas: List[StepData] = []
    __session: HttpSession = None
    __session_variables: VariablesMapping = {}
    __session_headers: Headers = {}
    # time
    __start_at: float = 0
    __duration: float = 0
    # log
    __log__: Text = ""

    def __init_tests__(self):
        self.__teststeps = []
        for step in self.teststeps:
            # step parameters
            if step.parameters:
                try:
                    parameters = parse_parameters(step.parameters)
                    for p_index, param in enumerate(parameters):
                        p_step = copy.deepcopy(step)
                        p_step.variables.update(param)
                        self.__teststeps.append(p_step)
                except exceptions.ParamsError as err:
                    self.message = repr(err)
                    self.success = False

                    logger.error(traceback.format_exc())

            else:
                self.__teststeps.append(step)

    @property
    def raw_testcase(self) -> TestCase:
        if not hasattr(self, "config"):
            self.__init_tests__()

        return TestCase(config=self.config, teststeps=self.__teststeps)

    # def with_project_meta(self, project_meta: ProjectMeta) -> "ZeroRunner":
    #     self.__project_meta = project_meta
    #     return self

    def with_functions(self, function_map: FunctionsMapping):
        self.config.functions.update(function_map)

    def with_session(self, session: HttpSession) -> "ZeroRunner":
        self.__session = session
        return self

    def with_case_id(self, case_id: Text) -> "ZeroRunner":
        self.__case_id = case_id
        return self

    def with_variables(self, variables: VariablesMapping, cover=False) -> "ZeroRunner":
        if cover:
            self.__session_variables = variables
        else:
            self.__session_variables.update(variables)
        return self

    def with_headers(self, headers: Headers, cover=False) -> "ZeroRunner":
        if cover:
            self.__session_headers.update(headers)
        else:
            self.__session_headers = headers
        return self

    def with_export(self, export: List[Text]) -> "ZeroRunner":
        self.__export = export
        return self

    def with_log(self, message: Text) -> "ZeroRunner":
        self.__log__ = f"{self.__log__}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:{message}"

        return self

    def __call_hooks(
            self, hooks: Hooks, step_variables: VariablesMapping, hook_msg: Text,
    ):
        """ 调用钩子.

        Args:
            hooks (list): 包含可能是字符串，控制器.

                format1 (str): 执行单个函数.
                    ${func()}
                format2 (dict): dict格式 执行函数并赋值给变量
                    {"var": "${func()}"}

            step_variables: current step variables to call hook, include two special variables

                request: parsed request dict
                response: ResponseObject for current response

            hook_msg: setup/teardown request/testcase

        """
        logger.info(f"call hook actions: {hook_msg}")

        if not isinstance(hooks, List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        for (index, hook) in enumerate(hooks):
            if isinstance(hook, Text):
                # format 1: ["${func()}"]
                logger.debug(f"call hook function: {hook}")
                parse_data(hook, step_variables, self.config.functions)
            elif isinstance(hook, Dict) and len(hook) == 1:
                # format 2: {"var": "${func()}"}
                var_name, hook_content = list(hook.items())[0]
                hook_content_eval = parse_data(
                    hook_content, step_variables, self.config.functions
                )
                logger.debug(
                    f"call hook function: {hook_content}, got value: {hook_content_eval}"
                )
                logger.debug(f"assign variable: {var_name} = {hook_content_eval}")
                step_variables[var_name] = hook_content_eval
            elif isinstance(hook, TStep):
                self.__run_step_request(hook)
            elif isinstance(hook, TStepController):
                step_type = hook.step_type
                if step_type == TStepTypeEnum.wait.value:
                    self.__run_step_wait(hook)
                elif step_type == TStepTypeEnum.sql.value:
                    self.__run_step_sql(hook)
                elif step_type == TStepTypeEnum.script.value:
                    self.__run_step_script(hook)

            else:
                logger.error(f"Invalid hook format: {hook}")

    def __run_step_request(self, step: TStep) -> StepData:
        """执行用例请求"""
        self.with_log(f"用例[{step.name}]开始")
        step_data = StepData(name=step.name, case_id=step.case_id)

        # parse
        prepare_upload_step(step, self.config.functions)
        request_dict = step.request.dict()
        request_dict.pop("upload", None)
        session_success = False
        # 初始化resp_obj
        resp_obj = None
        # 捕获异常
        try:
            # setup hooks
            if step.setup_hooks:
                self.with_log("前置脚本执行开始~~~")
                self.__call_hooks(step.setup_hooks, step.variables, "setup request")
                self.with_log("前置脚本执行结束~~~")

            # override variables  优先级 step.variables > self.config.variables > self.config.env_variables
            # merge_env_variables  合并环境变量
            step.variables = merge_variables(step.variables, self.config.env_variables)
            # step variables > 合并用例变量
            step.variables = merge_variables(step.variables, self.config.variables)
            # step variables > 合并提取变量
            step.variables = merge_variables(step.variables, self.extracted_variables)
            step.variables = merge_variables(step.variables, self.__session_variables)

            # parse variables
            step.variables = parse_variables_mapping(
                step.variables, self.config.functions
            )

            parsed_request_dict = parse_data(
                request_dict, step.variables, self.config.functions
            )

            # parsed_request_dict["headers"].setdefault(
            #     "Request-ID",
            #     f"{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
            # )
            step.variables["request"] = parsed_request_dict

            # prepare arguments
            method = parsed_request_dict.pop("method")
            url_path = parsed_request_dict.pop("url")
            url = build_url(self.config.base_url, url_path)
            parsed_request_dict["verify"] = self.config.verify
            parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})
            # 更新会话请求头
            self.__session_headers = parse_data(
                self.__session_headers,
                step.variables | self.__session_variables,
                self.config.functions
            )
            parsed_request_dict["headers"].update(self.__session_headers)

            # request
            resp = self.__session.request(method, url, **parsed_request_dict)
            resp_obj = ResponseObject(resp)
            step.variables["response"] = resp_obj

            # teardown hooks
            if step.teardown_hooks:
                self.with_log("后置脚本执行开始~~~")
                self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")
                self.with_log("后置脚本执行结束~~~")

            def log_req_resp_details():
                err_msg = "\n{} DETAILED REQUEST & RESPONSE {}\n".format("*" * 32, "*" * 32)

                # log request
                err_msg += "====== request details ======\n"
                err_msg += f"url: {url}\n"
                err_msg += f"method: {method}\n"
                headers = parsed_request_dict.pop("headers", {})
                err_msg += f"headers: {headers}\n"
                for k, v in parsed_request_dict.items():
                    v = utils.omit_long_data(v)
                    err_msg += f"{k}: {repr(v)}\n"

                err_msg += "\n"

                # log response
                err_msg += "====== response details ======\n"
                err_msg += f"status_code: {resp.status_code}\n"
                err_msg += f"headers: {resp.headers}\n"
                err_msg += f"body: {repr(resp.text)}\n"
                logger.error(err_msg)

            # extract
            extractors = step.extract
            extract_mapping = resp_obj.extract(extractors, step.variables, self.config.functions)
            step_data.export_vars = extract_mapping

            variables_mapping = step.variables
            variables_mapping.update(extract_mapping)

            # validate

            validators = step.validators

            try:
                resp_obj.validate(
                    validators, variables_mapping, self.config.functions
                )
                session_success = True
            except ValidationFailure:
                session_success = False
                log_req_resp_details()
                # log testcase duration before raise ValidationFailure
                self.__duration = time.time() - self.__start_at
                raise
        except Exception as err:
            err_info = traceback.format_exc()
            logger.error(err_info)
            session_success = False
            step_data.message = err_info

        finally:
            self.success = session_success
            step_data.success = session_success
            step_data.variables = step.variables
            step_data.case_id = step.case_id

            if hasattr(self.__session, "data"):
                # ZeroRunner.client.HttpSession, not locust.clients.HttpSession
                # save request & response meta data
                self.__session.data.success = session_success
                self.__session.data.validators = resp_obj.validation_results if resp_obj else {}

                # save step data
                step_data.data = self.__session.data
        self.with_log(f"用例[{step.name}]结束")
        return step_data

    def __run_step_sql(self, step: TStepController) -> StepData:
        """执行sql控制器"""
        self.with_log(f"sql控制器[{step.name}]开始")
        step_data = StepData(name=step.name)
        step_data.success = False
        step_data.status = "fail"
        try:
            db_info = DB(
                host=step.host,
                port=step.port,
                user=step.user,
                password=step.password,
                database=None
            )
            data = db_info.execute(step.value)
            step_data.success = True
            step_data.status = "success"
            variables = {step.variable_name: data}
            self.with_variables(variables)
            step_data.export_vars.update(variables)
            logger.info(f"SQL查询---> {step.value}")
            self.with_log(f"SQL查询-> 设置变量:{step.variable_name}, 设置变量值：{data}")
        except Exception as err:
            self.with_log(f"sql控制器执行错误:\n{err}")
            pass
        self.with_log(f"sql控制器[{step.name}]结束")
        return step_data

    def __run_step_wait(self, step: TStepController) -> StepData:
        """执行等待控制器"""
        self.with_log(f"等待控制器[{step.name}]开始")
        step_data = StepData(name=step.name)
        step_data.status = "skip"
        step_data.success = False
        if step.enable and step.value:
            time.sleep(step.value)
            step_data.success = True
            step_data.status = "success"
            logger.info(f"等待控制器---> {step.value}m")
            self.with_log(f"等待控制器---> {step.value}m")
        self.with_log(f"等待控制器[{step.name}]结束")
        return step_data

    def __run_step_script(self, step: TStepController):
        """执行脚本"""
        self.with_log(f"脚本步骤[{step.name}]开始")
        step_data = StepData(name=step.name)
        module_name = uuid.uuid4().hex

        base_script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "script_code.py")
        logger.info(os.getcwd())
        logger.info(os.path.abspath(os.path.dirname(__file__)))
        with open(base_script_path, 'r', encoding='utf8') as f:
            base_script = f.read()
        script = f"{base_script}\n{step.value}"
        script_module = load_script_content(script,
                                            f"script_{module_name}")
        headers = script_module.zero.headers.get_headers()
        variables = script_module.zero.environment.get_environment()
        for key, value in headers.items():
            self.with_log(f"设置请求头-> key:{key} value: {value}")
        for key, value in variables.items():
            self.with_log(f"设置请变量-> key:{key} value: {value}")
        self.with_headers(headers)
        self.with_variables(variables)
        functions = load_module_functions(script_module)
        self.with_functions(functions)
        # self.__session_variables.update(script_module.zero.environment.get_environment())
        step_data.success = True
        step_data.status = "success"
        self.with_log(f"脚本步骤[{step.name}]结束")
        return step_data

    def __run_step_testcase(self, step: TStep) -> StepData:
        """run teststep: referenced testcase"""
        step_data = StepData(name=step.name)
        step_variables = step.variables
        step_export = step.export

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step_variables, "setup testcase")

        if hasattr(step.testcase, "config") and hasattr(step.testcase, "teststeps"):
            testcase_cls = step.testcase
            case_result = (
                testcase_cls()
                .with_session(self.__session)
                .with_case_id(self.__case_id)
                .with_variables(step_variables)
                .with_export(step_export)
                .run()
            )

        # elif isinstance(step.testcase, Text):
        #     if os.path.isabs(step.testcase):
        #         ref_testcase_path = step.testcase
        #     else:
        #         ref_testcase_path = os.path.join(
        #             self.__project_meta.RootDir, step.testcase
        #         )
        #
        #     case_result = (
        #         ZeroRunner()
        #         .with_session(self.__session)
        #         .with_case_id(self.__case_id)
        #         .with_variables(step_variables)
        #         .with_export(step_export)
        #         .run_path(ref_testcase_path)
        #     )

        else:
            raise exceptions.ParamsError(
                f"Invalid teststep referenced testcase: {step.dict()}"
            )

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown testcase")

        step_data.data = case_result.get_step_datas()  # list of step data
        step_data.export_vars = case_result.get_export_variables()
        step_data.success = case_result.success
        self.success = case_result.success

        if step_data.export_vars:
            logger.info(f"export variables: {step_data.export_vars}")

        return step_data

    def __run_step(self, step: Union[TStep, TStepController]) -> Dict:
        """run teststep, teststep maybe a request or referenced testcase"""
        logger.info(f"run step begin: {step.name} >>>>>>")
        self.with_log(f"执行步骤->{step.name} >>>>>>")

        if isinstance(step, TStep):
            step_data = self.__run_step_request(step)
        elif isinstance(step, TStepController):
            step_type = step.step_type
            if step_type == TStepTypeEnum.wait.value:
                step_data = self.__run_step_wait(step)
            elif step_type == TStepTypeEnum.sql.value:
                step_data = self.__run_step_sql(step)
            elif step_type == TStepTypeEnum.script.value:
                step_data = self.__run_step_script(step)
            # elif step.testcase:
            #     step_data = self.__run_step_testcase(step)
        else:
            raise ParamsError(
                f"teststep is neither a request nor a referenced testcase: {step.dict()}"
            )

        self.__step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")
        self.with_log(f"步骤执行完成->{step.name} <<<<<<")
        return step_data.export_vars

    def __parse_config(self, config: TConfig):
        config.variables.update(self.__session_variables)
        config.variables = parse_variables_mapping(
            config.variables, self.config.functions
        )
        config.name = parse_data(
            config.name, config.variables, self.config.functions
        )
        config.base_url = parse_data(
            config.base_url, config.variables, self.config.functions
        )

    def run_testcase(self, testcase: TestCase) -> "ZeroRunner":
        """run specified testcase

        Examples:
            >>> testcase_obj = TestCase(config=TConfig(...), teststeps=[TStep(...)])
            >>> ZeroRunner().run_testcase(testcase_obj)

        """
        self.config = testcase.config
        self.__teststeps = testcase.teststeps

        # 参数初始化
        self.__parse_config(self.config)
        self.__start_at = time.time()
        self.__step_datas: List[StepData] = []
        self.__session = self.__session or HttpSession()
        # save extracted variables of teststeps
        self.extracted_variables: VariablesMapping = {}

        # run teststeps
        for index, step in enumerate(self.__teststeps):
            # 运行步骤
            extract_mapping = self.__run_step(step)

            # 保存提取的变量
            self.extracted_variables.update(extract_mapping)

        self.__session_variables.update(self.extracted_variables)
        self.__duration = time.time() - self.__start_at
        return self

    def run(self) -> "ZeroRunner":
        """ 运行用例"""
        self.__init_tests__()
        testcase_obj = TestCase(config=self.config, teststeps=self.__teststeps)
        return self.run_testcase(testcase_obj)

    def get_step_datas(self) -> List[StepData]:
        return self.__step_datas

    def get_export_variables(self) -> Dict:
        # override testcase export vars with step export
        export_var_names = self.__export or self.config.export
        export_vars_mapping = {}
        for var_name in export_var_names:
            if var_name not in self.__session_variables:
                raise ParamsError(
                    f"failed to export variable {var_name} from session variables {self.__session_variables}"
                )

            export_vars_mapping[var_name] = self.__session_variables[var_name]

        return export_vars_mapping

    def get_summary(self) -> TestCaseSummary:
        """get testcase result summary"""
        start_at_timestamp = self.__start_at
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
        testcase_summary = TestCaseSummary(
            name=self.config.name,
            success=self.success,
            message=self.message,
            case_id=self.__case_id,
            time=TestCaseTime(
                start_at=self.__start_at,
                start_at_iso_format=start_at_iso_format,
                duration=self.__duration,
            ),
            in_out=TestCaseInOut(
                config_vars=self.config.variables,
                # export_vars=self.get_export_variables(),
            ),
            log=self.__log__,
            step_datas=self.__step_datas,
        )
        return testcase_summary

    def test_start(self, param: Dict = None) -> "ZeroRunner":
        """主入口"""
        self.__init_tests__()
        self.__case_id = self.__case_id or str(uuid.uuid4())

        log_handler = logger.add(sys.stdin, level="INFO")

        # parse config name
        config_variables = self.config.variables
        if param:
            config_variables.update(param)
        config_variables.update(self.__session_variables)
        self.config.name = parse_data(
            self.config.name, config_variables, self.config.functions
        )

        logger.info(
            f"Start to run testcase: {self.config.name}, TestCase ID: {self.__case_id}"
        )

        try:
            return self.run_testcase(
                TestCase(config=self.config, teststeps=self.__teststeps)
            )
        finally:
            logger.remove(log_handler)
