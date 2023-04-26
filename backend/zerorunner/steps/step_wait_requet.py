# -*- coding: utf-8 -*-
# @author: xiaobai

import time

from loguru import logger
from zerorunner.model.base import TStepLogType, TStepResultStatusEnum
from zerorunner.model.result_model import StepResult
from zerorunner.model.step_model import TStep
from zerorunner.runner_new import SessionRunner
from zerorunner.steps.base import IStep


def run_wait_request(runner: SessionRunner,
                     step: TStep,
                     step_tag: str = None,
                     parent_step_result: StepResult = None):
    """等待控制器"""
    step.name = "等待控制器"
    step_result = runner.get_step_result(step)
    runner.set_run_log(step_result=step_result, log_type=TStepLogType.start)
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.wait_request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    try:
        wait_time = parsed_request_dict.get("wait_time", None)
        if wait_time or wait_time == 0:
            time.sleep(wait_time)
            logger.info(f"等待控制器---> {wait_time}m")
            runner.set_run_log(f"等待控制器---> {wait_time}m")
            step_result.step_tag = f"wait[{wait_time}m]"
            runner.set_step_result_status(step_result, TStepResultStatusEnum.success)

        else:
            raise ValueError("等待时间不能为空！")
    except Exception as err:
        runner.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        raise
    finally:
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
        runner.set_run_log(step_result=step_result, log_type=TStepLogType.end)


class WaitWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_wait_time(self, wait_time: int) -> "WaitWithOptionalArgs":
        self.__step.wait_request.wait_time = wait_time
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
