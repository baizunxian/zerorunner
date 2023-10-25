# -*- coding: utf-8 -*-
# @author: xiao bai
import os
import time
import uuid

from zerorunner.loader import load_script_content, load_module_functions
from zerorunner.models.base import TStepLogType, TStepResultStatusEnum
from zerorunner.models.result_model import StepResult
from zerorunner.models.step_model import TStep, TScriptRequest
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult


def run_script_request(runner: SessionRunner,
                       step: TStep,
                       step_tag: str = None,
                       parent_step_result: TStepResult = None):
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    try:
        step.request = TScriptRequest.parse_obj(parsed_request_dict)
        module_name = uuid.uuid4().hex
        model, captured_output = load_script_content(step.request.script_content, f"script_{module_name}")
        step_result.set_step_log_not_show_time(captured_output)
        functions = load_module_functions(model)
        runner.with_functions(functions)
        step_result.set_step_result_status(TStepResultStatusEnum.success)
    except Exception as exc:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise exc
    finally:
        step_result.end_log()
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
