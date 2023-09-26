# -*- coding: utf-8 -*-
# @author: xiao bai
import os
import time
import uuid

from zerorunner.loader import load_script_content, load_module_functions
from zerorunner.model.base import TStepLogType, TStepResultStatusEnum
from zerorunner.model.result_model import StepResult
from zerorunner.model.step_model import TStep, TScriptRequest
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult


def run_script_request(runner: SessionRunner,
                       step: TStep,
                       step_tag: str = None,
                       parent_step_result: StepResult = None):
    step_result = TStepResult(step, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.script_request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    step.script_request = TScriptRequest(**parsed_request_dict)
    try:
        module_name = uuid.uuid4().hex
        base_script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "script_code.py")
        with open(base_script_path, 'r', encoding='utf8') as f:
            base_script = f.read()
        script = f"{base_script}\n\n{step.script_request.script_content}"
        script_module, _ = load_script_content(script, f"script_{module_name}")
        headers = script_module.zero.headers.get_headers()
        variables = script_module.zero.environment.get_environment()
        for key, value in headers.items():
            step_result.set_step_log(f"✏️设置请求头-> key:{key} value: {value}")
        for key, value in variables.items():
            step_result.set_step_log(f"✏️设置请变量-> key:{key} value: {value}")
        runner.with_session_variables(variables)
        functions = load_module_functions(script_module)
        runner.with_functions(functions)
    except Exception as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)


class ScriptWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_script_content(self, script_content: int) -> "ScriptWithOptionalArgs":
        self.__step.script_request.script_content = script_content
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
