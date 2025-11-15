# -*- coding: utf-8 -*-
# @author: 小白
import time
import uuid

import requests

from zerorunner import exceptions
from zerorunner.models.base import TStepResultStatusEnum
from zerorunner.models.result_model import SessionData, PyScriptResponseData
from zerorunner.models.step_model import TStep, TScriptRequest
from zerorunner.response import ResponseObject, ResponseData
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult
from zerorunner.utils import parser_json


def run_script_request(runner: SessionRunner,
                       step: TStep,
                       step_tag: str = None,
                       parent_step_result: TStepResult = None):
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    # step_variables = runner.get_merge_variable(step)
    request_dict = step.request.dict()
    step_variables = runner.get_merge_variable(step)

    resp_obj = None

    try:
        parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
        step_result.result.session_data = SessionData()
        step.request = TScriptRequest(**parsed_request_dict)
        # setup hooks
        if step.setup_hooks:
            step_result.set_step_log("前置hook开始~~~")
            runner.run_hooks(hooks=step.setup_hooks, hook_msg="setup_hooks", parent_step_result=step_result)
            step_result.set_step_log("前置hook结束~~~")

        if step.setup_code:
            # setup code
            try:
                step_result.set_step_log("前置code开始~~~")
                runner.run_script(script=step.setup_code, step=step)
                step_result.set_step_log(f"前置code结束  ~~~")
            except Exception as e:
                raise exceptions.MyBaseError(f"前置code执行失败: {e}")

        step_result.result.session_data.request = step.request
        if not step.request.script_content:
            raise exceptions.TestCaseSkip("🪂脚本为空跳过执行~")
        run_start_time = time.time()
        model, _ = runner.run_script(script=step.request.script_content, step=step)
        run_duration = round((time.time() - run_start_time) * 1000, 2)
        result = getattr(model, "result", None)
        step_result.result.session_data.response = PyScriptResponseData(result=result)
        step_result.result.session_data.stat.response_time_ms = run_duration
        step_result.result.session_data.stat.content_size = len(str(result))

        resp_data = ResponseData(
            duration=run_duration,
            json_data=parser_json(result),
            text=parser_json(result, False),
        )

        resp_obj = ResponseObject(resp_data, step_type=step.step_type, parser=runner.parser)

        # 提取
        extract_mapping = resp_obj.extract(step.extracts)
        runner.with_session_variables(extract_mapping)

        # teardown code
        if step.teardown_code:
            try:
                step_result.set_step_log(f"后置code开始~~~")
                runner.run_script(script=step.teardown_code, step=step)
                step_result.set_step_log("后置code结束~~~")
            except Exception as e:
                raise exceptions.MyBaseError(f"后置code执行失败: {e}")

        # teardown hooks
        if step.teardown_hooks:
            step_result.set_step_log("后置hook开始~~~")
            runner.run_hooks(hooks=step.teardown_hooks, hook_msg="teardown_hooks", parent_step_result=step_result)
            step_result.set_step_log("后置hook结束~~~")

        # 断言
        resp_obj.validate(step.validators, runner.get_merge_variable_pool())

        # step_result.set_step_log_not_display_time(script_output)
        step_result.set_step_result_status(TStepResultStatusEnum.success)

    except exceptions.MyBaseFailure as err:
        step_result.set_step_result_status(TStepResultStatusEnum.fail)
        raise
    except exceptions.TestCaseSkip as err:
        step_result.set_step_result_status(TStepResultStatusEnum.skip, str(err))
        raise
    except (Exception, exceptions.MyBaseError) as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise
    except Exception as exc:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        step_result.result.session_data.success = False
        raise exc

    finally:
        step_result.end_log()
        # step_result.set_variable_pool(runner.get_variable_pool(parser=False))
        if resp_obj:
            step_result.result.session_data.validators = resp_obj.validation_results
            step_result.result.session_data.extracts = resp_obj.extract_results
        step_result = step_result.get_step_result()
        if parent_step_result:
            parent_step_result.set_step_log_not_show_time(step_result.log)
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)


class ScriptWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_script_content(self, script_content: int) -> "ScriptWithOptionalArgs":
        self.__step.request.script_content = script_content
        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def run(self, runner: SessionRunner, **kwargs):
        return run_script_request(runner, self.__step, **kwargs)


class RunScriptStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_script_request(runner, self.__step, **kwargs)
