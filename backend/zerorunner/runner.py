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
from copy import deepcopy
from datetime import datetime
from typing import List, Dict, Text, Any, Union, Iterable

from loguru import logger

from zerorunner import exceptions
from zerorunner import utils
from zerorunner.client import HttpSession
from zerorunner.exceptions import ValidationFailure, ParamsError, LoopNotFound
from zerorunner.ext.db import DB
from zerorunner.ext.uploader import prepare_upload_step
from zerorunner.loader import load_script_content, load_module_functions
from zerorunner.models import (
    TConfig,
    TCaseController,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseInOut,
    TestCase,
    Hooks, FunctionsMapping, Headers, TController,
    TSqlController,
    TWaitController,
    TScriptController, TIFController, TLoopController, LoopTypeEnum, TStepDataStatusEnum, TStepLogType,
    TStepControllerDict, )
from zerorunner.parser import parse_variables_mapping, parse_data, build_url, parse_parameters, get_mapping_function, \
    parse_string_value
from zerorunner.response import ResponseObject, uniform_validator
from zerorunner.snowflake import id_center
from zerorunner.utils import merge_variables


class ZeroRunner(object):
    config: TConfig
    teststeps: List[Any]

    extracted_variables: VariablesMapping = {}
    success: bool = False  # indicate testcase execution result
    message: Text = ""  # 错误信息或备注等信息记录
    __case_id: Text = ""
    __teststeps: List[Any]
    __export: List[Text] = []
    __step_datas: List[StepData] = []
    __session: HttpSession = None
    __session_variables: VariablesMapping = {}
    __session_headers: Headers = {}
    # time
    __start_time: float = 0
    __duration: float = 0
    # count
    __run_count: int = 0  # 运行的步骤数
    __actual_run_count: int = 0  # 实际运行的步骤数  可能循环控制 多次执行
    __run_success_count: int = 0  # 运行成功数
    __run_fail_count: int = 0  # 运行失败数
    __run_err_count: int = 0  # 运行错误数
    __run_skip_count: int = 0  # 运行跳过数
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

    def __set_run_log(self, message: Text = None, step_data: StepData = None, log_type: TStepLogType = None):
        """
        args :
            message: 日志内容
            log_type: 内容类型 start end  success fail skip err 等
        """
        log_header = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:"
        if step_data and log_type:
            content = f"{TStepControllerDict[step_data.step_type]} -> {step_data.name} {log_type}"
            if log_type == TStepLogType.start:
                message = f"▶️ {content}"
            if log_type == TStepLogType.end:
                message = f"⏹️ {content}"
            if log_type == TStepLogType.success:
                message = f"✔️ {content}"
            if log_type == TStepLogType.fail:
                message = f"❌ {content}"
            if log_type == TStepLogType.skip:
                message = f"⏭️ {content}"
            if log_type == TStepLogType.wait:
                message = f"⏱️ {content}"
            if log_type == TStepLogType.loop:
                message = f"🔄 {content}"
            if log_type == TStepLogType.condition:
                message = f" {content}"
            if log_type == TStepLogType.err:
                message = f"❗ {content} -> {step_data.message}"
        if message:
            self.__log__ += f"{log_header}{message}\n"

    def __call_hooks(
            self,
            hooks: Hooks,
            parent_step: TController,
            hook_type: Text,
    ) -> Union[List[StepData], Any]:
        """ 调用钩子.

        Args:
            hooks (list): 包含可能是字符串，控制器.

                format1 (str): 执行单个函数.
                    ${func()}
                format2 (dict): dict格式 执行函数并赋值给变量
                    {"var": "${func()}"}

            parent_step.variables: current step variables to call hook, include two special variables

                request: parsed request dict
                response: ResponseObject for current response

            hook_type: pre 前置  post后置

        """
        logger.info(f"call hook actions: {hook_type}")

        if not isinstance(hooks, List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        step_data_list = []
        for (index, hook) in enumerate(hooks):
            step_data = self.__run_step_controller(hook, parent_step, hook_type)
            step_data_list.append(step_data)
        return step_data_list

    def __run_step_request(self, step: TCaseController, parent_step: TController, step_tag: Text = None) -> StepData:
        """执行用例请求"""

        step_data = self.__get_step_data(step, parent_step, step_tag)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.start)
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
                self.__set_run_log(f"{step_data.name} 前置脚本执行开始~~~")
                pre_step_data_list = self.__call_hooks(step.setup_hooks, step, "pre")
                step_data.pre_hook_data = pre_step_data_list

                self.__set_run_log(f"{step_data.name} 前置脚本执行结束~~~")

            # override variables  优先级
            """
            __session_variables(会话变量) > extracted_variables(提取变量) > step.variables(用例变量) >
            config.env_variables(环境变量)
            
            """
            # 合并用例变量
            merge_variable = merge_variables(self.config.env_variables, self.config.variables)
            # 合并用例变量
            step.variables = merge_variables(step.variables, self.__session_variables)
            merge_variable = merge_variables(merge_variable, step.variables)
            # 合并提取变量
            merge_variable = merge_variables(merge_variable, self.extracted_variables)

            # parse variables
            merge_variable = parse_variables_mapping(
                merge_variable, self.config.functions
            )
            self.__session_variables = merge_variable

            parsed_request_dict = parse_data(
                request_dict, merge_variable, self.config.functions
            )

            parsed_request_dict["headers"].setdefault(
                "Request-ID",
                f"{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
            )
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
                merge_variable | self.__session_variables,
                self.config.functions
            )
            parsed_request_dict["headers"].update(self.__session_headers)

            # request
            resp = self.__session.request(method, url, **parsed_request_dict)
            resp_obj = ResponseObject(resp)
            step.variables["response"] = resp_obj

            # teardown hooks
            if step.teardown_hooks:
                self.__set_run_log(f"{step_data.name} 后置脚本执行开始~~~")
                post_step_list = self.__call_hooks(step.teardown_hooks, step, "post")
                step_data.post_hook_data = post_step_list
                # 提取步骤的提取参数同步到用例
                for step_data_item in post_step_list:
                    if step_data_item.step_type == 'extract':
                        step_data.export_vars.update(step_data_item.export_vars)
                self.__set_run_log(f"{step_data.name} 后置脚本执行结束~~~")

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

            # variables_mapping = step.variables

            # extract
            extractors = step.extracts
            extract_mapping = resp_obj.extract(extractors, step.variables, self.config.functions)
            step_data.export_vars = extract_mapping

            merge_variable.update(extract_mapping)

            # validate
            validators = step.validators

            try:
                resp_obj.validate(
                    validators, merge_variable, self.config.functions
                )
                session_success = True
            except ValidationFailure as err:
                session_success = False
                self.__set_step_data_status(step_data, TStepDataStatusEnum.fail, str(err))
                log_req_resp_details()
                # log testcase duration before raise ValidationFailure
                # self.__duration = time.time() - self.__start_time
        except Exception as err:
            err_info = traceback.format_exc()
            logger.error(err_info)
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        finally:
            step_data.env_variables = self.config.env_variables
            step_data.variables = step.variables
            step_data.case_id = step.case_id

            if hasattr(self.__session, "data"):
                # ZeroRunner.client.HttpSession, not locust.clients.HttpSession
                # save request & response meta data
                self.__session.data.success = session_success
                self.__session.data.validators = resp_obj.validation_results if resp_obj else {}

                # save step data
                step_data.session_data = self.__session.data
        # 前后置步骤判断用例是否失败
        step_success = True
        for step_info in step_data.pre_hook_data:
            if step_info.success is False:
                step_success = False
        for step_info in step_data.post_hook_data:
            if step_info.success is False:
                step_success = False

        self.__set_step_data_status(step_data,
                                    TStepDataStatusEnum.success if step_success else TStepDataStatusEnum.fail)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __run_step_sql(self, step: TSqlController, parent_step: TController, step_tag: Text = None) -> StepData:
        """执行sql控制器"""
        step_data = self.__get_step_data(step, parent_step, step_tag)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.start)
        try:
            db_info = DB(
                host=step.host,
                port=step.port,
                user=step.user,
                password=step.password,
                database=None
            )
            data = db_info.execute(step.value)
            variables = {step.variable_name: data}
            self.with_variables(variables)
            step_data.export_vars.update(variables)
            logger.info(f"SQL查询---> {step.value}")
            self.__set_run_log(f"SQL查询-> 设置变量:{step.variable_name}, 设置变量值：{data}")
        except Exception as err:
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        self.__set_step_data_status(step_data, TStepDataStatusEnum.success)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __run_step_wait(self, step: TWaitController, parent_step: TController, step_tag: Text = None) -> StepData:
        """等待控制器"""
        step.name = "等待控制器"
        step_data = self.__get_step_data(step, parent_step, step_tag)
        try:
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.start)
            if step.value:
                time.sleep(step.value)
                logger.info(f"等待控制器---> {step.value}m")
                self.__set_run_log(f"等待控制器---> {step.value}m")
        except Exception as err:
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        self.__set_step_data_status(step_data, TStepDataStatusEnum.success)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __run_step_script(self, step: TScriptController, parent_step: TController, step_tag: Text = None) -> StepData:
        """执行脚本控制器"""

        step_data = self.__get_step_data(step, parent_step, step_tag)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.start)

        try:
            module_name = uuid.uuid4().hex
            base_script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "script_code.py")
            logger.info(os.getcwd())
            logger.info(os.path.abspath(os.path.dirname(__file__)))
            with open(base_script_path, 'r', encoding='utf8') as f:
                base_script = f.read()
            script = f"{base_script}\n\n{step.value}"
            script_module = load_script_content(script, f"script_{module_name}")
            headers = script_module.zero.headers.get_headers()
            variables = script_module.zero.environment.get_environment()
            for key, value in headers.items():
                self.__set_run_log(f"✏️设置请求头-> key:{key} value: {value}")
            for key, value in variables.items():
                self.__set_run_log(f"✏️设置请变量-> key:{key} value: {value}")
            self.with_headers(headers)
            self.with_variables(variables)
            functions = load_module_functions(script_module)
            self.with_functions(functions)
        except Exception as err:
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        self.__set_step_data_status(step_data, TStepDataStatusEnum.success)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __run_step_if(self, step: TIFController, parent_step: TController,
                      step_tag: Text = None) -> StepData:
        """条件控制器"""
        step.name = "条件控制器"
        step_data = self.__get_step_data(step, parent_step, step_tag)
        try:
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.start)
            step_data.step_data = []
            if not step.comparator:
                self.__set_step_data_status(step_data, TStepDataStatusEnum.fail, "条件控制器--> 条件不能为空！")
                return step_data
            c_result = self.__comparators(step.check, step.expect, step.comparator)
            if c_result.get("check_result", "fail") == "success":
                self.__execute_loop(step.teststeps, step_data)
            else:
                self.__set_step_data_status(step_data, TStepDataStatusEnum.fail, f"😑条件不满足跳过跳过 ---> {c_result}")
                self.__set_run_log(f"条件不符---> {c_result.get('validate_msg', '')}")
                return step_data
        except Exception as err:
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        self.__set_step_data_status(step_data, TStepDataStatusEnum.success)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __run_step_loop(self, step: TLoopController, parent_step: TController, step_tag: Text = None) -> StepData:
        """循环控制器"""
        step.name = "循环控制器"
        step_data = self.__get_step_data(step, parent_step, step_tag)
        step_data.step_data = []
        try:
            if not step.teststeps:
                self.__set_step_data_status(step_data, TStepDataStatusEnum.skip, "循环控制器没有子步骤跳过")
                return step_data

            # 次数循环
            if step.loop_type.lower() == LoopTypeEnum.Count.value:
                self.__set_run_log(f"🔄次数循环---> 开始")
                for i in range(min(step.count_number, 100)):
                    self.__execute_loop(step.teststeps, step_data)
                    self.__set_run_log(f"次数循环---> 第{i + 1}次")

                    time.sleep(step.count_sleep_time)
                self.__set_run_log(f"次数循环---> 结束")

            # for 循环
            elif step.loop_type.lower() == LoopTypeEnum.For.value:
                for_variable_name = step.for_variable_name
                iterable_obj = parse_data(step.for_variable, self.__session_variables, self.config.functions)
                if not isinstance(iterable_obj, Iterable):
                    self.__set_run_log(f"for 循环错误： 变量 {iterable_obj} 不是一个可迭代对象！")
                    return step_data
                self.__set_run_log(f"🔄for循环---> 开始")
                for for_variable_value in iterable_obj:
                    self.with_variables({for_variable_name: for_variable_value})
                    self.__execute_loop(step.teststeps, step_data)
                    time.sleep(step.for_sleep_time)
                self.__set_run_log(f"🔄for循环---> 结束")

            # while 循环  最大循环次数 100
            elif step.loop_type.lower() == LoopTypeEnum.While.value:
                # todo 循环超时时间待实现
                run_number = 0
                self.__set_run_log(f"🔄while循环---> 开始")
                while True:
                    c_result = self.__comparators(step.while_variable, step.while_value, step.while_comparator)
                    if c_result.get("check_result", "fail") == "success":
                        self.__set_run_log(f"条件符合退出while循环 ---> {c_result}")
                        break
                    self.__set_run_log(f"条件不满足继续while循环 ---> {c_result}")
                    self.__execute_loop(step.teststeps, step_data)
                    run_number += 1
                    if run_number > 100:
                        self.__set_run_log(f"循环次数大于100退出while循环")
                        break
                    time.sleep(step.while_sleep_time)
                self.__set_run_log(f"🔄while循环---> 结束")
            else:
                self.__set_step_data_status(step_data, TStepDataStatusEnum.fail,
                                            "😑请确认循环类型是否为 count for while")
                self.__set_run_log(step_data=step_data, log_type=TStepLogType.fail)
                raise LoopNotFound("请确认循环类型是否为 count for while ")
        except Exception as err:
            self.__set_step_data_status(step_data, TStepDataStatusEnum.err, str(err))
            return step_data
        self.__set_step_data_status(step_data, TStepDataStatusEnum.success)
        self.__set_run_log(step_data=step_data, log_type=TStepLogType.end)
        return step_data

    def __execute_loop(self, teststeps: List[TController], parent_step_data: StepData):
        """执行循环"""
        for teststep in teststeps:
            # 循环会导致 循环下的步骤的step_id 一致，这里重新赋值，保证step_id唯一
            teststep.step_id = id_center.get_id()
            son_step_data = self.__run_step_controller(teststep)
            self.__session_variables.update(son_step_data.export_vars)
            parent_step_data.step_data.append(deepcopy(son_step_data))

    def __run_step_controller(self, step: TController, parent_step: TController = None,
                              step_tag: Text = None) -> StepData:
        """执行控制器"""

        if not step.enable:
            step_data = self.__get_step_data(step, parent_step, step_tag)
            self.__set_step_data_status(step_data, TStepDataStatusEnum.skip, "跳过")
            return step_data
        if isinstance(step, TCaseController):
            step_data = self.__run_step_request(step, parent_step, step_tag)
        elif isinstance(step, TWaitController):
            step_data = self.__run_step_wait(step, parent_step, step_tag)
        elif isinstance(step, TSqlController):
            step_data = self.__run_step_sql(step, parent_step, step_tag)
        elif isinstance(step, TScriptController):
            step_data = self.__run_step_script(step, parent_step, step_tag)
        elif isinstance(step, TIFController):
            step_data = self.__run_step_if(step, parent_step, step_tag)
        elif isinstance(step, TLoopController):
            step_data = self.__run_step_loop(step, parent_step)
        else:
            raise ParamsError(
                f"测试步骤不是一个用例😅: {step.dict()}"
            )
        step_data.duration = time.time() - step_data.start_time
        self.__actual_run_count += 1
        return step_data

    def __set_step_data_status(self, step_data: StepData, status: TStepDataStatusEnum, msg: Text = ""):
        """设置步骤状态"""

        if status == TStepDataStatusEnum.success:
            step_data.success = True
            step_data.status = TStepDataStatusEnum.success.value
            step_data.message = msg
            self.__run_success_count += 1
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.success)

        if status == TStepDataStatusEnum.fail:
            step_data.success = False
            step_data.status = TStepDataStatusEnum.fail.value
            step_data.message = msg
            self.__run_fail_count += 1
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.fail)

        if status == TStepDataStatusEnum.skip:
            step_data.success = True
            step_data.status = TStepDataStatusEnum.skip.value
            step_data.message = msg if msg else "跳过"
            self.__run_skip_count += 1
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.skip)

        if status == TStepDataStatusEnum.err:
            step_data.success = False
            step_data.status = TStepDataStatusEnum.err.value
            step_data.message = msg
            self.__run_err_count += 1
            self.__set_run_log(step_data=step_data, log_type=TStepLogType.err)

        if self.__run_fail_count == 0 and self.__run_err_count == 0:
            self.success = True
        else:
            self.success = False

    @staticmethod
    def __get_step_data(step: TController, parent_step: TController = None, step_tag: Text = None):
        """步初始化骤结果对象"""
        step_data = StepData(name=step.name,
                             step_type=step.step_type,
                             step_id=step.step_id,
                             start_time=time.time(),
                             step_tag=step_tag,
                             parent_step_id=parent_step.step_id if parent_step else None
                             )
        if hasattr(step, "case_id"):
            step_data.case_id = step.case_id
        return step_data

    def __run_step(self, step: TController, parent_step: TController = None) -> Dict:
        """运行步骤，可能是用例，可能是步骤控制器"""
        logger.info(f"run step begin: {step.name} >>>>>>")
        self.__set_run_log(f"执行步骤->{step.name} >>>>>>")

        step_data = self.__run_step_controller(step, parent_step, "controller")
        self.__run_count += 1
        self.__step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")
        self.__set_run_log(f"步骤执行完成->{step.name} <<<<<<")
        return step_data.export_vars

    def __comparators(self, check: Text, expect: Text, comparator: Text) -> Dict[Text, Any]:
        """
        结果比较
        """
        check_value = parse_data(check, self.__session_variables, self.config.functions)
        expect_value = parse_data(expect, self.__session_variables, self.config.functions)
        # check_value = parse_string_value(check_value)
        expect_value = parse_string_value(expect_value)
        u_validator = uniform_validator({"check": check_value, "expect": expect_value, "comparator": comparator})
        assert_method = u_validator["assert"]
        assert_func = get_mapping_function(assert_method, self.config.functions)
        validator_dict = {
            "comparator": assert_method,
            "check": check,
            "check_value": check_value,
            "expect": expect,
            "expect_value": expect_value,
            "check_result": "fail",
            "validate_msg": ""
        }
        try:
            assert_func(check_value, expect_value)
            validator_dict["check_result"] = "success"
        except AssertionError as ex:
            validator_dict["check_result"] = "fail"
            validate_msg = ""
            validate_msg += "\t==> fail"
            validate_msg += (
                f"\n"
                f"check_item: {check}\n"
                f"check_value: {check_value}({type(check_value).__name__})\n"
                f"assert_method: {assert_method}\n"
                f"expect_value: {expect_value}({type(expect_value).__name__})"
            )
            validator_dict["validate_msg"] = validate_msg

        return validator_dict

    def __parse_config(self, config: TConfig):
        """解析配置"""
        config.variables.update(self.__session_variables)
        config.variables = parse_variables_mapping(config.variables, self.config.functions)
        config.name = parse_data(config.name, config.variables, self.config.functions)
        config.base_url = parse_data(config.base_url, config.variables, self.config.functions)
        self.with_case_id(config.case_id)

    def run_testcase(self, testcase: TestCase) -> "ZeroRunner":
        """run specified testcase

        Examples:
            >>> testcase_obj = TestCase(config=TConfig(...), teststeps=[TCaseController(...)])
            >>> ZeroRunner().run_testcase(testcase_obj)

        """
        logger.info("用例开始执行 🚀")
        self.config = testcase.config
        self.__teststeps = testcase.teststeps

        # 参数初始化
        self.__parse_config(self.config)
        self.__start_time = time.time()
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
        self.__duration = time.time() - self.__start_time
        return self

    def run(self) -> "ZeroRunner":
        """ 运行用例"""
        self.__init_tests__()
        testcase_obj = TestCase(config=self.config, teststeps=self.teststeps)
        return self.run_testcase(testcase_obj)

    def get_step_datas(self) -> List[StepData]:
        """获取步骤"""
        return self.__step_datas

    def get_export_variables(self) -> Dict:
        """获取导出的变量"""
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
        """获取测试用例结果摘要"""
        start_at_timestamp = self.__start_time
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
        testcase_summary = TestCaseSummary(
            name=self.config.name,
            success=self.success,
            message=self.message,
            case_id=self.__case_id,
            start_time=self.__start_time,
            start_time_iso_format=start_at_iso_format,
            run_count=self.__run_count,
            actual_run_count=self.__actual_run_count,
            run_success_count=self.__run_success_count,
            run_fail_count=self.__run_fail_count,
            run_skip_count=self.__run_skip_count,
            run_err_count=self.__run_err_count,
            duration=self.__duration,
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


class HandleStepData:
    """设置步骤状态"""

    @staticmethod
    def success(step_data: StepData, msg: Text = ""):
        step_data.success = True
        step_data.status = "success"
        step_data.message = msg

    @staticmethod
    def skip(step_data: StepData, msg: Text = ""):
        step_data.success = True
        step_data.status = "skip"
        step_data.message = msg

    @staticmethod
    def fail(step_data: StepData, msg: Text = ""):
        step_data.success = False
        step_data.status = "fail"
        step_data.message = msg

    @staticmethod
    def err(step_data: StepData, msg: Text = ""):
        step_data.success = False
        step_data.status = "err"
        step_data.message = msg
