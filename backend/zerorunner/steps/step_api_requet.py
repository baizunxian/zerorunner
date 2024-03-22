# -*- coding: utf-8 -*-
# @author: xiaobai
import copy
import time
import traceback
import typing
from unittest import SkipTest

import requests
from loguru import logger

from autotest.utils.local import g
from zerorunner import exceptions, utils
from zerorunner.ext.uploader import prepare_upload_step
from zerorunner.loader import load_script_content
from zerorunner.models.base import TStepResultStatusEnum, Hooks
from zerorunner.models.result_model import StepResult
from zerorunner.models.step_model import TStep
from zerorunner.models.step_model import VariablesMapping, TRequest, MethodEnum
from zerorunner.parser import build_url, Parser
from zerorunner.response import ResponseObject
from zerorunner.runner import SessionRunner
from zerorunner.script_code import Zero
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult


def call_hooks(
        runner: SessionRunner,
        hooks: Hooks,
        step_variables: VariablesMapping,
        hook_msg: str,
        parent_step_result: TStepResult
) -> typing.Union[typing.List[StepResult], typing.Any]:
    """ 调用钩子.

    Args:
        runner (list): 包含可能是字符串，控制器.
        hook_msg (list): 包含可能是字符串，控制器.
        parent_step_result (list): 包含可能是字符串，控制器.
        step_variables (list): 包含可能是字符串，控制器.
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
            runner.parser.parse_data(hook, step_variables)
        elif isinstance(hook, typing.Dict) and len(hook) == 1:
            # format 2: {"var": "${func()}"}
            var_name, hook_content = list(hook.items())[0]
            hook_content_eval = runner.parser.parse_data(
                hook_content, step_variables
            )
            logger.debug(
                f"call hook function: {hook_content}, got value: {hook_content_eval}"
            )
            logger.debug(f"assign variable: {var_name} = {hook_content_eval}")
            step_variables[var_name] = hook_content_eval
        elif hasattr(hook, "run"):
            try:
                runner.run_step(hook, step_tag=hook_msg, parent_step_result=parent_step_result)
            except Exception:
                logger.error(traceback.format_exc())
                continue
        else:
            logger.error(f"Invalid hook format: {hook}")


def run_api_request(runner: SessionRunner,
                    step: TStep,
                    step_tag: str = None,
                    parent_step_result: TStepResult = None):
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    # update headers
    merge_headers = copy.deepcopy(runner.config.headers)
    merge_headers.update(step.request.headers)
    step.request.headers = merge_headers
    session_success = False
    # 初始化resp_obj
    resp_obj = None
    extract_mapping = {}
    # 捕获异常
    try:
        runner.handle_skip_feature(step)
        # 合并变量
        merge_variable = runner.get_merge_variable(step=step)
        # parse
        upload_variables = prepare_upload_step(step, runner.config.functions, merge_variable)
        request_dict = step.request.dict()
        request_dict.pop("upload", None)

        # setup hooks
        if step.setup_hooks:
            step_result.set_step_log("前置hook开始~~~")
            call_hooks(runner=runner,
                       hooks=step.setup_hooks,
                       step_variables=merge_variable,
                       hook_msg="setup_hooks",
                       parent_step_result=step_result)
            step_result.set_step_log("前置hook结束~~~")
        # setup code
        if step.setup_code:
            step_result.set_step_log("前置code开始~~~")
            zero = Zero(runner=runner,
                        step=step,
                        request=request_dict,
                        environment=runner.config.env_variables,
                        variables=step.variables)
            _, captured_output = load_script_content(content=step.setup_code,
                                                     module_name=f"{runner.config.case_id}_setup_code",
                                                     params={"zero": zero, "requests": requests})
            if captured_output:
                step_result.set_step_log("前置code输出: \n" + captured_output)
            step_result.set_step_log(f"前置code结束  ~~~")

        # 前置步骤后再执行下合并 避免前置步骤中复制变量获取不到
        merge_variable = runner.get_merge_variable(step=step)
        if upload_variables:
            merge_variable = {key: value for key, value in merge_variable.items()}
            merge_variable.update(runner.parser.parse_variables(upload_variables))

        parsed_request_dict = runner.parser.parse_data(
            request_dict, merge_variable
        )

        parsed_request_dict["headers"].setdefault("Z-Case-Id", runner.case_id)
        parsed_request_dict["headers"].setdefault("Z-Request-Id", f"{g.trace_id}")
        parsed_request_dict["headers"] = headers_to_str(parsed_request_dict["headers"])
        step.variables["request"] = parsed_request_dict

        # prepare arguments
        method = parsed_request_dict.pop("method")
        url_path = parsed_request_dict.pop("url")
        url = build_url(runner.config.base_url, url_path)
        parsed_request_dict["verify"] = runner.config.verify
        # request
        resp = runner.session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp, parser=Parser(functions_mapping=runner.config.functions))
        step.variables["response"] = resp_obj

        def log_req_resp_details():
            err_msg = "\n{:*^64}\n".format("DETAILED REQUEST & RESPONSE")

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
            err_msg += f"body: {repr(resp)}\n"
            logger.error(err_msg)

        # extract
        extractors = step.extracts
        extract_mapping = resp_obj.extract(extractors, merge_variable, runner.config.functions)
        step_result.result.export_vars = extract_mapping
        merge_variable.update(extract_mapping)

        # teardown code
        if step.teardown_code:
            step_result.set_step_log(f"后置code开始  ~~~")
            zero = Zero(runner=runner,
                        step=step,
                        request=request_dict,
                        response=resp_obj,
                        environment=runner.config.env_variables,
                        variables=step.variables
                        )
            _, captured_output = load_script_content(step.teardown_code,
                                                     f"{runner.config.case_id}_teardown_code",
                                                     params={"zero": zero, "requests": requests, 'res': resp_obj})
            if captured_output:
                step_result.set_step_log("后置code输出: \n" + captured_output)
            # code  执行完成后重新合并变量
            merge_variable = runner.get_merge_variable(step=step)
            step_result.set_step_log("后置code结束~~~")

        # teardown hooks
        if step.teardown_hooks:
            step_result.set_step_log("后置hook开始~~~")
            call_hooks(runner=runner,
                       hooks=step.teardown_hooks,
                       step_variables=merge_variable,
                       hook_msg="teardown_hooks",
                       parent_step_result=step_result)
            step_result.set_step_log("后置hook结束~~~")
            # code teardown 执行完成后重新合并变量
            merge_variable = runner.get_merge_variable(step=step)

        # validate
        validators = step.validators

        try:
            resp_obj.validate(
                validators, merge_variable
            )
            session_success = True
            step_result.set_step_result_status(TStepResultStatusEnum.success)
        except exceptions.ValidationFailure as err:
            session_success = False
            step_result.set_step_result_status(TStepResultStatusEnum.fail)
            log_req_resp_details()
            # log testcase duration before raise ValidationFailure
            raise

    except exceptions.MyBaseError as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise

    except SkipTest as err:
        step_result.set_step_result_status(TStepResultStatusEnum.skip)
        raise

    except Exception as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise

    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        step_result.env_variables = runner.config.env_variables
        step_result.case_variables = runner.config.variables
        step_result.variables = step.variables
        step_result.session_data = runner.get_session_variables()
        # step_result.case_id = step.case_id
        step_result.duration = time.time() - step_result.start_time

        if hasattr(runner.session, "data"):
            # ZeroRunner.client.HttpSession, not locust.clients.HttpSession
            # save request & response meta data
            runner.session.data.success = session_success
            runner.session.data.validators = resp_obj.validation_results if resp_obj else {}
            runner.session.data.extracts = resp_obj.extract_results if resp_obj else []

            # save step data
            step_result.session_data = runner.session.data
        runner.extracted_variables.update(extract_mapping)
        runner.with_session_variables(runner.extracted_variables)
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)


def headers_to_str(headers: dict):
    if headers and isinstance(headers, dict):
        return {str(key): str(value) for key, value in headers.items()}


class StepRequestValidation(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def assert_equal(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append({"equal": [jmes_path, expected_value, message]})
        return self

    def assert_not_equal(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"not_equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_greater_than(
            self, jmes_path: str, expected_value: typing.Union[int, float], message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"greater_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_less_than(
            self, jmes_path: str, expected_value: typing.Union[int, float], message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"less_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_greater_or_equals(
            self, jmes_path: str, expected_value: typing.Union[int, float], message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"greater_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_less_or_equals(
            self, jmes_path: str, expected_value: typing.Union[int, float], message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"less_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_equal(
            self, jmes_path: str, expected_value: int, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"length_equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_greater_than(
            self, jmes_path: str, expected_value: int, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"length_greater_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_less_than(
            self, jmes_path: str, expected_value: int, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"length_less_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_greater_or_equals(
            self, jmes_path: str, expected_value: int, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"length_greater_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_less_or_equals(
            self, jmes_path: str, expected_value: int, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"length_less_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_string_equals(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"string_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_startswith(
            self, jmes_path: str, expected_value: str, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"startswith": [jmes_path, expected_value, message]}
        )
        return self

    def assert_endswith(
            self, jmes_path: str, expected_value: str, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"endswith": [jmes_path, expected_value, message]}
        )
        return self

    def assert_regex_match(
            self, jmes_path: str, expected_value: str, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"regex_match": [jmes_path, expected_value, message]}
        )
        return self

    def assert_contains(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"contains": [jmes_path, expected_value, message]}
        )
        return self

    def assert_contained_by(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"contained_by": [jmes_path, expected_value, message]}
        )
        return self

    def assert_type_match(
            self, jmes_path: str, expected_value: typing.Any, message: str = ""
    ) -> "StepRequestValidation":
        self.__step.validators.append(
            {"type_match": [jmes_path, expected_value, message]}
        )
        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return f"request-{self.__step.request.method}"

    def run(self, runner: SessionRunner, **kwargs):
        return run_api_request(runner, self.__step)


class StepRequestExtraction(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_jmespath(self, jmes_path: str, var_name: str) -> "StepRequestExtraction":
        self.__step.extract[var_name] = jmes_path
        return self

    # def with_regex(self):
    #     # TODO: extract response html with regex
    #     pass
    #
    # def with_jsonpath(self):
    #     # TODO: extract response json with jsonpath
    #     pass

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self.__step)

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return f"request-{self.__step.request.method}"

    def run(self, runner: SessionRunner, **kwargs):
        return run_api_request(runner, self.__step)


class RequestWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_params(self, **params) -> "RequestWithOptionalArgs":
        self.__step.request.params.update(params)
        return self

    def with_headers(self, **headers) -> "RequestWithOptionalArgs":
        self.__step.request.headers.update(headers)
        return self

    def with_cookies(self, **cookies) -> "RequestWithOptionalArgs":
        self.__step.request.cookies.update(cookies)
        return self

    def with_data(self, data) -> "RequestWithOptionalArgs":
        self.__step.request.data = data
        return self

    def with_json(self, req_json) -> "RequestWithOptionalArgs":
        self.__step.request.req_json = req_json
        return self

    def set_timeout(self, timeout: float) -> "RequestWithOptionalArgs":
        self.__step.request.timeout = timeout
        return self

    def set_verify(self, verify: bool) -> "RequestWithOptionalArgs":
        self.__step.request.verify = verify
        return self

    def set_allow_redirects(self, allow_redirects: bool) -> "RequestWithOptionalArgs":
        self.__step.request.allow_redirects = allow_redirects
        return self

    def upload(self, **file_info) -> "RequestWithOptionalArgs":
        self.__step.request.upload.update(file_info)
        return self

    def teardown_hook(
            self, hook: str, assign_var_name: str = None
    ) -> "RequestWithOptionalArgs":
        if assign_var_name:
            self.__step.teardown_hooks.append({assign_var_name: hook})
        else:
            self.__step.teardown_hooks.append(hook)

        return self

    def extract(self) -> StepRequestExtraction:
        return StepRequestExtraction(self.__step)

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self.__step)

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return f"request-{self.__step.request.method}"

    def run(self, runner: SessionRunner, **kwargs):
        return run_api_request(runner, self.__step)


class RunRequest(object):
    def __init__(self, name: str):
        self.__step = TStep(name=name)

    def with_step(self, step: TStep):
        self.__step = step
        return self

    def with_variables(self, **variables) -> "RunRequest":
        self.__step.variables.update(variables)
        return self

    def with_retry(self, retry_times, retry_interval) -> "RunRequest":
        self.__step.retry_times = retry_times
        self.__step.retry_interval = retry_interval
        return self

    def setup_hook(self, hook: str, assign_var_name: str = None) -> "RunRequest":
        if assign_var_name:
            self.__step.setup_hooks.append({assign_var_name: hook})
        else:
            self.__step.setup_hooks.append(hook)

        return self

    def get(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.GET, url=url)
        return RequestWithOptionalArgs(self.__step)

    def post(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.POST, url=url)
        return RequestWithOptionalArgs(self.__step)

    def put(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.PUT, url=url)
        return RequestWithOptionalArgs(self.__step)

    def head(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.HEAD, url=url)
        return RequestWithOptionalArgs(self.__step)

    def delete(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.DELETE, url=url)
        return RequestWithOptionalArgs(self.__step)

    def options(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.OPTIONS, url=url)
        return RequestWithOptionalArgs(self.__step)

    def patch(self, url: str) -> RequestWithOptionalArgs:
        self.__step.request = TRequest(method=MethodEnum.PATCH, url=url)
        return RequestWithOptionalArgs(self.__step)


class RunRequestStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_api_request(runner, self.__step, **kwargs)
