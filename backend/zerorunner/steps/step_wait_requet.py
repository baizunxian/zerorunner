# -*- coding: utf-8 -*-
# @author: xiao bai

import time

from loguru import logger

from zerorunner.models.base import TStepResultStatusEnum
from zerorunner.models.step_model import TStep
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult


def run_wait_request(runner: SessionRunner,
                     step: TStep,
                     step_tag: str = None,
                     parent_step_result: TStepResult = None):
    """等待控制器"""
    step.name = "等待控制器"
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    try:
        wait_time = parsed_request_dict.get("wait_time", None)
        if wait_time or wait_time == 0:
            time.sleep(wait_time)
            logger.info(f"等待控制器---> {wait_time}s")
            step_result.set_step_log(f"等待控制器---> {wait_time}s")
            step_result.step_tag = f"wait[{wait_time}s]"
            step_result.set_step_result_status(TStepResultStatusEnum.success)

        else:
            raise ValueError("等待时间不能为空！")
    except Exception as exc:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise exc
    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        if parent_step_result:
            parent_step_result.set_step_log(step_result.log, show_time=False)
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)


class WaitWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_wait_time(self, wait_time: int) -> "WaitWithOptionalArgs":
        self.__step.request.wait_time = wait_time
        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def run(self, runner: SessionRunner, **kwargs):
        return run_wait_request(runner, self.__step, **kwargs)


class RunWaitStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_wait_request(runner, self.__step, **kwargs)
