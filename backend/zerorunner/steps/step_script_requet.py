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
    step.request = TScriptRequest.parse_obj(parsed_request_dict)
    try:
        module_name = uuid.uuid4().hex
        script = f"{step.request.script_content}"
        model, captured_output = load_script_content(step.request.script_content,
                                                     f"{runner.config.case_id}_setup_code")
        script_module, _ = load_script_content(script, f"script_{module_name}")
        functions = load_module_functions(model)
        runner.with_functions(functions)
    except Exception as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        if parent_step_result:
            parent_step_result.set_step_log(step_result.log, show_time=False)
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
