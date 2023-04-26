# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import os
import sys
import time
import traceback
import typing
import uuid
from datetime import datetime

from loguru import logger

from zerorunner import utils, exceptions
from zerorunner.client import HttpSession
from zerorunner.ext.db import DB
from zerorunner.ext.uploader import prepare_upload_step
from zerorunner.loader import load_script_content, load_module_functions
from zerorunner.model.step_model import TStep
from zerorunner.models import (
    TConfig,
    TApiController,
    VariablesMapping,
    StepResult,
    TestCaseSummary,
    TestCaseInOut,
    TestCase,
    Hooks, FunctionsMapping, TController,
    TSqlController,
    TWaitController,
    TScriptController, TIFController, TLoopController, LoopTypeEnum, TStepResultStatusEnum, TStepLogType,
    TStepControllerDict, )
from zerorunner.parser import parse_variables_mapping, parse_data, build_url, get_mapping_function, \
    parse_string_value, Parser
from zerorunner.response import ResponseObject, uniform_validator
from zerorunner.snowflake import id_center
from zerorunner.utils import merge_variables


class SessionRunner(object):
    config: TConfig
    teststeps: typing.List[typing.Any]

    parser: Parser = None
    case_id: str = ""
    extracted_variables: VariablesMapping = {}
    session: HttpSession = None
    # 错误信息或备注等信息记录
    message: str = ""

    __teststeps: typing.List[typing.Any]
    __export: typing.List[str] = []
    __step_results: typing.List[StepResult] = []
    __session_variables: VariablesMapping = {}
    # __session_headers: Headers = {}
    # time
    __start_time: float = 0
    __duration: float = 0
    # log
    __log__: str = ""

    def __init(self):
        self.__config = self.config
        self.__session_variables = self.__session_variables or {}
        self.__start_at = 0
        self.__duration = 0

        self.case_id = self.case_id or str(uuid.uuid4())
        self.__step_results = self.__step_results or []
        self.session = self.session or HttpSession()
        self.parser = self.parser or Parser(self.config.functions)

    def __init_tests__(self):
        # 参数初始化
        self.__teststeps = []
        self.message = ""
        self.__start_time = time.time()
        self.__duration = 0
        # self.__session = self.__session or HttpSession()
        self.__session = HttpSession()
        self.__session_variables = {}
        self.__step_results: typing.List[StepResult] = []
        self.__log__ = ""
        # self.extracted_variables: VariablesMapping = {}

    def with_config(self, config: TConfig) -> "SessionRunner":
        self.config = config
        return self

    def with_functions(self, function_map: FunctionsMapping) -> "SessionRunner":
        self.config.functions.update(function_map)
        return self

    def with_session(self, session: HttpSession) -> "SessionRunner":
        self.session = session
        return self

    def with_case_id(self, case_id: typing.Union[str, int]) -> "SessionRunner":
        self.case_id = case_id
        return self

    def with_variables(self, variables: VariablesMapping, cover=False) -> "SessionRunner":
        if cover:
            self.__session_variables = variables
        else:
            self.__session_variables.update(variables)
        return self

    def with_session_variables(self, variables: VariablesMapping, cover=False) -> "SessionRunner":
        if cover:
            self.__session_variables = variables
        else:
            self.__session_variables.update(variables)
        return self

    # def with_headers(self, headers: Headers, cover=False) -> "SessionRunner":
    #     if cover:
    #         self.__session_headers.update(headers)
    #     else:
    #         self.__session_headers = headers
    #     return self

    def with_export(self, export: typing.List[str]) -> "SessionRunner":
        self.__export = export
        return self

    def get_session_variables(self):
        return self.__session_variables

    def set_run_log(self, message: str = None, step_result: StepResult = None, log_type: TStepLogType = None):
        """
        args :
            message: 日志内容
            log_type: 内容类型 start end  success fail skip err 等
        """
        log_header = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:"
        if step_result and log_type:
            content = f"{TStepControllerDict[step_result.step_type]} -> {step_result.name} {log_type}"
            if log_type == TStepLogType.start:
                msg = f"▶️ {content}"
            elif log_type == TStepLogType.end:
                msg = f"⏹️ {content}"
            elif log_type == TStepLogType.success:
                msg = f"✔️ {content}"
            elif log_type == TStepLogType.fail:
                msg = f"❌ {content}"
            elif log_type == TStepLogType.skip:
                msg = f"⏭️ {content}"
            elif log_type == TStepLogType.wait:
                msg = f"⏱️ {content}"
            elif log_type == TStepLogType.loop:
                msg = f"🔄 {content}"
            elif log_type == TStepLogType.condition:
                msg = f" {content}"
            elif log_type == TStepLogType.err:
                msg = f"❗ {content} -> {message}"
            else:
                msg = ""
            step_result.log += f"{log_header}{msg}\n"
            self.__log__ += f"{log_header}{msg}\n"

    def __call_hooks(
            self,
            hooks: Hooks,
            step_variables: VariablesMapping,
            hook_msg: str,
            parent_step_result: StepResult
    ) -> typing.Union[typing.List[StepResult], typing.Any]:
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
        logger.info(f"call hook actions: {hook_msg}")

        if not isinstance(hooks, typing.List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        for hook in hooks:
            if isinstance(hook, str):
                # format 1: ["${func()}"]
                logger.debug(f"call hook function: {hook}")
                parse_data(hook, step_variables, self.config.functions)
            elif isinstance(hook, typing.Dict) and len(hook) == 1:
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
            elif isinstance(hook, (TApiController,
                                   TScriptController,
                                   TSqlController,
                                   TWaitController,
                                   TLoopController,
                                   TIFController,
                                   TestCase)):
                try:
                    self.run_step(hook, step_tag=hook_msg, parent_step_result=parent_step_result)
                except Exception:
                    continue
            else:
                logger.error(f"Invalid hook format: {hook}")

    def __run_step_request(self, step: TApiController, step_tag=None, parent_step_result: StepResult = None):
        """执行用例请求"""

        step_result = self.get_step_result(step, step_tag=step_tag)
        self.set_run_log(step_result=step_result, log_type=TStepLogType.start)
        # parse
        prepare_upload_step(step, self.config.functions)
        request_dict = step.request.dict()
        request_dict.pop("upload", None)
        session_success = False
        extract_mapping = {}
        # 初始化resp_obj
        resp_obj = None
        # 捕获异常
        try:
            # 合并变量
            merge_variable = self.get_merge_variable(step)

            # parse variables
            merge_variable = parse_variables_mapping(
                merge_variable, self.config.functions
            )
            # self.__session_variables = merge_variable

            # setup hooks
            if step.setup_hooks:
                self.set_run_log(f"{step_result.name} setup hooks start~~~")
                self.__call_hooks(hooks=step.setup_hooks,
                                  step_variables=merge_variable,
                                  hook_msg="setup_hooks",
                                  parent_step_result=step_result)
                self.set_run_log(f"{step_result.name} setup hooks end~~~")

            parsed_request_dict = parse_data(
                request_dict, merge_variable, self.config.functions
            )

            parsed_request_dict["headers"].setdefault(
                "Request-ID",
                f"{self.case_id}-{str(int(time.time() * 1000))[-6:]}",
            )
            step.variables["request"] = parsed_request_dict

            # prepare arguments
            method = parsed_request_dict.pop("method")
            url_path = parsed_request_dict.pop("url")
            url = build_url(self.config.base_url, url_path)
            parsed_request_dict["verify"] = self.config.verify
            parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})
            # 更新会话请求头
            # self.__session_headers = parse_data(
            #     self.__session_headers,
            #     merge_variable | self.__session_variables,
            #     self.config.functions
            # )
            # parsed_request_dict["headers"].update(self.__session_headers)

            # request
            resp = self.__session.request(method, url, **parsed_request_dict)
            resp_obj = ResponseObject(resp, parser=Parser(functions_mapping=self.config.functions))
            step.variables["response"] = resp_obj

            # teardown hooks
            if step.teardown_hooks:
                self.set_run_log(f"{step_result.name} teardown hooks start~~~")
                self.__call_hooks(hooks=step.teardown_hooks,
                                  step_variables=merge_variable,
                                  hook_msg="teardown_hooks",
                                  parent_step_result=step_result)
                self.set_run_log(f"{step_result.name} teardown hooks end~~~")

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
            step_result.export_vars = extract_mapping

            merge_variable.update(extract_mapping)

            # validate
            validators = step.validators

            try:
                resp_obj.validate(validators=validators, variables_mapping=merge_variable)
                session_success = True
                self.set_step_result_status(step_result, TStepResultStatusEnum.success)
            except exceptions.ValidationFailure as err:
                session_success = False
                self.set_step_result_status(step_result, TStepResultStatusEnum.fail, str(err))
                log_req_resp_details()
                # log testcase duration before raise ValidationFailure
                raise
        except exceptions.MyBaseError as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise

        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise

        finally:
            step_result.env_variables = self.config.env_variables
            step_result.case_variables = self.config.variables
            step_result.variables = step.variables
            step_result.session_data = self.__session_variables
            step_result.case_id = step.case_id
            step_result.duration = time.time() - step_result.start_time

            if hasattr(self.__session, "data"):
                # ZeroRunner.client.HttpSession, not locust.clients.HttpSession
                # save request & response meta data
                self.__session.data.success = session_success
                self.__session.data.validators = resp_obj.validation_results if resp_obj else {}

                # save step data
                step_result.session_data = self.__session.data
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.extracted_variables.update(extract_mapping)
            self.__session_variables.update(self.extracted_variables)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __run_step_sql(self, step: TSqlController, step_tag: str = None, parent_step_result: StepResult = None):
        """执行sql控制器"""
        step_result = self.get_step_result(step, step_tag)
        start_time = time.time()
        self.set_run_log(step_result=step_result, log_type=TStepLogType.start)
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
            step_result.export_vars.update(variables)
            logger.info(f"SQL查询---> {step.value}")
            self.set_run_log(f"SQL查询-> 设置变量:{step.variable_name}, 设置变量值：{data}")
            self.set_step_result_status(step_result, TStepResultStatusEnum.success)
        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, traceback.format_exc())
            raise
        finally:
            step_result.duration = time.time() - start_time
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __run_step_wait(self, step: TWaitController, step_tag: str = None, parent_step_result: StepResult = None):
        """等待控制器"""
        step.name = "等待控制器"
        step_result = self.get_step_result(step)
        start_time = time.time()
        try:
            self.set_run_log(step_result=step_result, log_type=TStepLogType.start)
            if step.value or step.value == 0:
                time.sleep(step.value)
                logger.info(f"等待控制器---> {step.value}m")
                self.set_run_log(f"等待控制器---> {step.value}m")
                step_result.step_tag = f"wait[{step.value}]m]"
                self.set_step_result_status(step_result, TStepResultStatusEnum.success)

            else:
                raise ValueError("等待时间不能为空！")
        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise
        finally:
            step_result.duration = time.time() - start_time
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __run_step_script(self, step: TScriptController, step_tag: str = None, parent_step_result: StepResult = None):
        """执行脚本控制器"""

        step_result = self.get_step_result(step, step_tag)
        start_time = time.time()
        self.set_run_log(step_result=step_result, log_type=TStepLogType.start)
        try:
            module_name = uuid.uuid4().hex
            base_script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "script_code.py")
            with open(base_script_path, 'r', encoding='utf8') as f:
                base_script = f.read()
            script = f"{base_script}\n\n{step.value}"
            script_module = load_script_content(script, f"script_{module_name}")
            headers = script_module.zero.headers.get_headers()
            variables = script_module.zero.environment.get_environment()
            for key, value in headers.items():
                self.set_run_log(f"✏️设置请求头-> key:{key} value: {value}")
            for key, value in variables.items():
                self.set_run_log(f"✏️设置请变量-> key:{key} value: {value}")
            # self.with_headers(headers)
            self.with_variables(variables)
            functions = load_module_functions(script_module)
            self.with_functions(functions)
        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        finally:
            step_result.duration = time.time() - start_time
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __run_step_if(self, step: TIFController, step_tag: str = None, parent_step_result: StepResult = None):
        """条件控制器"""
        step.name = "条件控制器"
        step_result = self.get_step_result(step, step_tag)
        start_time = time.time()
        self.set_run_log(step_result=step_result, log_type=TStepLogType.start)
        try:
            if not step.comparator:
                raise ValueError("条件控制器--> 条件不能为空！")
            c_result = self.__comparators(step.check, step.expect, step.comparator)
            check_value = c_result.get("check_value", "")
            if c_result.get("check_result", "fail") != "success":
                self.set_run_log(f"条件不符---> {c_result.get('validate_msg', '')}")
                raise exceptions.ValidationFailure(f"条件不符---> {c_result.get('validate_msg', '')}")
            try:
                self.__execute_loop(step.teststeps, step_tag=f"IF {check_value}")
            except Exception as err:
                pass

            self.set_step_result_status(step_result, TStepResultStatusEnum.success)
        except exceptions.VariableNotFound as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise
        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise

        finally:
            step_result.duration = time.time() - start_time
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __run_step_loop(self, step: TLoopController, step_tag: str = None, parent_step_result: StepResult = None):
        """循环控制器"""
        step.name = "循环控制器"
        step_result = self.get_step_result(step, step_tag)
        start_time = time.time()
        try:
            # 次数循环
            if step.loop_type.lower() == LoopTypeEnum.Count.value:
                self.set_run_log(f"🔄次数循环---> 开始")
                for i in range(min(step.count_number, 100)):
                    try:
                        self.__execute_loop(step.teststeps, step_tag=f"Loop {i + 1}")
                        self.set_run_log(f"次数循环---> 第{i + 1}次")
                        time.sleep(step.count_sleep_time)
                    except Exception as err:
                        logger.error(err)
                        continue
                self.set_run_log(f"次数循环---> 结束")

            # for 循环
            elif step.loop_type.lower() == LoopTypeEnum.For.value:
                for_variable_name = step.for_variable_name
                merge_variable = self.get_merge_variable()
                iterable_obj = parse_data(step.for_variable, merge_variable, self.config.functions)
                if not isinstance(iterable_obj, typing.Iterable):
                    self.set_run_log(f"for 循环错误： 变量 {iterable_obj} 不是一个可迭代对象！")
                    raise ValueError("for 循环错误： 变量 {iterable_obj} 不是一个可迭代对象！")
                self.set_run_log(f"🔄for循环---> 开始")
                for for_variable_value in iterable_obj:
                    try:
                        self.with_variables({for_variable_name: for_variable_value})
                        self.__execute_loop(step.teststeps, step_tag=f"For {for_variable_value}")
                        time.sleep(step.for_sleep_time)
                    except Exception as err:
                        logger.error(err)
                        continue
                self.set_run_log(f"🔄for循环---> 结束")

            # while 循环  最大循环次数 100
            elif step.loop_type.lower() == LoopTypeEnum.While.value:
                # todo 循环超时时间待实现
                run_number = 0
                self.set_run_log(f"🔄while循环---> 开始")
                while True:
                    c_result = self.__comparators(step.while_variable, step.while_value, step.while_comparator)
                    check_value = c_result.get("check_value", "")
                    if c_result.get("check_result", "fail") == "success":
                        self.set_run_log(f"条件符合退出while循环 ---> {c_result}")
                        break
                    self.set_run_log(f"条件不满足继续while循环 ---> {c_result}")
                    try:
                        self.__execute_loop(step.teststeps, step_tag=f"while {check_value}")
                    except Exception as err:
                        logger.error(err)
                        continue
                    run_number += 1
                    if run_number > 100:
                        self.set_run_log(f"循环次数大于100退出while循环")
                        break
                    time.sleep(step.while_sleep_time)
                self.set_run_log(f"🔄while循环---> 结束")
            else:
                raise exceptions.LoopNotFound("请确认循环类型是否为 count for while ")

        except Exception as err:
            self.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
            raise

        finally:
            step_result.duration = time.time() - start_time
            self.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
            self.set_run_log(step_result=step_result, log_type=TStepLogType.end)

    def __execute_loop(self, teststeps: typing.List[TController], step_tag=None, parent_step_result: StepResult = None):
        """执行循环"""
        for teststep in teststeps:
            # 循环会导致 循环下的步骤的step_id 一致，这里重新赋值，保证step_id唯一
            teststep.step_id = id_center.get_id()
            self.run_step(teststep, step_tag=step_tag, parent_step_result=parent_step_result)

    def set_step_result_status(self, step_result: StepResult, status: TStepResultStatusEnum, msg: str = ""):
        """设置步骤状态"""

        if status == TStepResultStatusEnum.success:
            step_result.success = True
            step_result.status = TStepResultStatusEnum.success.value
            step_result.message = msg
            self.set_run_log(step_result=step_result, log_type=TStepLogType.success)

        if status == TStepResultStatusEnum.fail:
            step_result.success = False
            step_result.status = TStepResultStatusEnum.fail.value
            step_result.message = msg
            self.set_run_log(step_result=step_result, log_type=TStepLogType.fail)

        if status == TStepResultStatusEnum.skip:
            step_result.success = True
            step_result.status = TStepResultStatusEnum.skip.value
            step_result.message = msg if msg else "跳过"
            self.set_run_log(step_result=step_result, log_type=TStepLogType.skip)

        if status == TStepResultStatusEnum.err:
            step_result.success = False
            step_result.status = TStepResultStatusEnum.err.value
            step_result.message = msg
            self.set_run_log(message=traceback.format_exc(), step_result=step_result, log_type=TStepLogType.err)

    def append_step_result(self, step_result: StepResult, step_tag: str, parent_step_result: StepResult):
        """setup_hooks teardown_hooks"""
        if parent_step_result:
            if step_tag and step_tag == "setup_hooks":
                parent_step_result.setup_hook_data.append(step_result)
            elif step_tag and step_tag == "teardown_hooks":
                parent_step_result.teardown_hook_data.append(step_result)
            else:
                parent_step_result.step_result.append(step_result)
        else:
            self.__step_results.append(step_result)

    @staticmethod
    def get_step_result(step: TStep, step_tag: str = None):
        """步初始化骤结果对象"""
        step_result = StepResult(name=step.name,
                                 step_type=step.step_type,
                                 start_time=time.time(),
                                 step_tag=step_tag,
                                 )
        if hasattr(step, "case_id"):
            step_result.case_id = step.case_id
        return step_result

    def run_step(self, step: TController, step_tag=None, parent_step_result: StepResult = None):
        """运行步骤，可能是用例，可能是步骤控制器"""
        logger.info(f"run step begin: {step.name} >>>>>>")
        self.set_run_log(f"执行步骤->{step.name} >>>>>>")

        if isinstance(step, TApiController):
            self.__run_step_request(step, step_tag=step_tag, parent_step_result=parent_step_result)
        elif isinstance(step, TWaitController):
            self.__run_step_wait(step, step_tag=step_tag, parent_step_result=parent_step_result)
        elif isinstance(step, TSqlController):
            self.__run_step_sql(step, step_tag=step_tag, parent_step_result=parent_step_result)
        elif isinstance(step, TScriptController):
            self.__run_step_script(step, step_tag=step_tag, parent_step_result=parent_step_result)
        elif isinstance(step, TIFController):
            self.__run_step_if(step, step_tag=step_tag, parent_step_result=parent_step_result)
        elif isinstance(step, TLoopController):
            self.__run_step_loop(step, step_tag=step_tag, parent_step_result=parent_step_result)
        else:
            raise exceptions.ParamsError(
                f"不是正确的步骤 😅: {step.dict()}"
            )
        # step_result = self.__run_step_controller(step, parent_step_result, "controller")
        # self.__run_count += 1
        logger.info(f"run step end: {step.name} <<<<<<\n")
        self.set_run_log(f"步骤执行完成->{step.name} <<<<<<")

    def __comparators(self, check: str, expect: str, comparator: str) -> typing.Dict[str, typing.Any]:
        """
        结果比较
        """
        merge_variable = self.get_merge_variable()

        check_value = parse_data(check, merge_variable, self.config.functions)
        expect_value = parse_data(expect, merge_variable, self.config.functions)
        expect_value = parse_string_value(expect_value)
        # check_value = parse_string_value(check_value)
        # expect_value = parse_string_value(expect_value)
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

    def get_merge_variable(self, step: TStep = None):
        """
        获取合并的变量
        优先级
        __session_variables(会话变量)
                V
        extracted_variables(提取变量)
                V
        step.variables(用例变量)
                V
        config.env_variables(环境变量)

        """

        # 合并用例变量
        merge_variable = merge_variables(self.config.env_variables, self.config.variables)
        # 合并用例变量
        if step:
            merge_variable = merge_variables(step.variables, merge_variable)
        merge_variable = merge_variables(self.__session_variables, merge_variable)
        # 合并提取变量
        merge_variable = merge_variables(self.extracted_variables, merge_variable)
        return merge_variable

    def __parse_config(self, config: TConfig):
        """解析配置"""
        config.variables.update(self.__session_variables)
        config.variables = parse_variables_mapping(config.variables, self.config.functions)
        config.name = parse_data(config.name, config.variables, self.config.functions)
        config.base_url = parse_data(config.base_url, config.variables, self.config.functions)
        # self.with_case_id(config.case_id)

    def run_testcase(self, testcase: typing.Union[TestCase, TController]) -> "SessionRunner":
        """run specified testcase

        Examples:
            >>> testcase_obj = TestCase(config=TConfig(...), teststeps=[TApiController(...)])
            >>> SessionRunner().run_testcase(testcase_obj)

        """
        logger.info("用例开始执行 🚀")

        self.__init_tests__()

        if isinstance(testcase, TestCase):
            self.config = testcase.config
            self.__parse_config(self.config)
            self.__teststeps = testcase.teststeps

            # run teststeps
            for index, step in enumerate(self.__teststeps):
                # 运行步骤
                if not step.enable:
                    logger.debug(f"禁用步骤跳过---> {step.name}")
                    continue
                self.run_step(step)
        elif isinstance(testcase, (TApiController,
                                   TScriptController,
                                   TSqlController,
                                   TWaitController,
                                   TLoopController,
                                   TIFController,)):
            self.run_step(testcase)
        else:
            raise
        #     # 保存提取的变量
        #     self.extracted_variables.update(extract_mapping)
        #
        # self.__session_variables.update(self.extracted_variables)
        self.__duration = time.time() - self.__start_time
        return self

    def run(self) -> "Runner":
        """ 运行用例"""
        # self.__init_tests__()
        testcase_obj = TestCase(config=self.config, teststeps=self.teststeps)
        return self.run_testcase(testcase_obj)

    def get_step_results(self) -> typing.List[StepResult]:
        """获取步骤"""
        return self.__step_results

    def get_export_variables(self) -> typing.Dict:
        """获取导出的变量"""
        # override testcase export vars with step export
        export_var_names = self.__export or self.config.export
        export_vars_mapping = {}
        for var_name in export_var_names:
            if var_name not in self.__session_variables:
                raise exceptions.ParamsError(
                    f"failed to export variable {var_name} from session variables {self.__session_variables}"
                )

            export_vars_mapping[var_name] = self.__session_variables[var_name]

        return export_vars_mapping

    def get_summary(self) -> TestCaseSummary:
        """获取测试用例结果摘要"""
        start_at_timestamp = self.__start_time
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()

        summary_success = True
        for step_result in self.__step_results:
            if not step_result.success:
                summary_success = False
                break

        testcase_summary = TestCaseSummary(
            name=self.config.name,
            success=summary_success,
            message=self.message,
            case_id=self.config.case_id,
            start_time=self.__start_time,
            start_time_iso_format=start_at_iso_format,
            duration=self.__duration,
            in_out=TestCaseInOut(
                config_vars=self.config.variables,
                # export_vars=self.get_export_variables(),
            ),
            log=self.__log__,
            step_results=self.__step_results,
        )
        return testcase_summary

    def test_start(self, param: typing.Dict = None) -> "SessionRunner":
        """主入口"""
        self.__init_tests__()
        self.case_id = self.case_id or str(uuid.uuid4())

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
            f"Start to run testcase: {self.config.name}, TestCase ID: {self.case_id}"
        )

        try:
            return self.run_testcase(
                TestCase(config=self.config, teststeps=self.__teststeps)
            )
        finally:
            logger.remove(log_handler)
