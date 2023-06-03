# -*- coding: utf-8 -*-
# @author: xiaobai

import time
import traceback

from loguru import logger
from zerorunner.model.base import TStepLogType, TStepResultStatusEnum
from zerorunner.model.result_model import StepResult, UiSessionData
from zerorunner.model.step_model import TStep, TUiRequest
from zerorunner.response import uniform_validator
from zerorunner.runner_new import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.ui_driver.keywords.web import WebAction


def run_ui_request(runner: SessionRunner,
                   step: TStep,
                   step_tag: str = None,
                   parent_step_result: StepResult = None):
    """运行ui request"""
    step_result = runner.get_step_result(step)
    step_result.ui_session_data = UiSessionData()
    step_result.ui_session_data.action = step.ui_request.action
    step_result.ui_session_data.location_value = step.ui_request.location_value
    step_result.ui_session_data.location_type = step.ui_request.location_type
    step_result.ui_session_data.input_data = step.ui_request.input_data

    runner.set_run_log(step_result=step_result, log_type=TStepLogType.start)
    start_time = time.time()
    step.variables.update(runner.driver_app.get_session_variables())
    step_variables = runner.get_merge_variable(step)
    request_dict = step.ui_request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    try:
        ui_step = TUiRequest(**parsed_request_dict)
        if not hasattr(WebAction, ui_step.action):
            logger.error(f"操作方法不存在： {ui_step.action}")
            raise AttributeError(f"操作方法不存在： {ui_step.action}")
        getattr(WebAction, ui_step.action)(runner.driver_app, ui_step)
        base64_png_data = runner.driver_app.get_screenshot()
        # step_result
        runner.set_step_result_status(step_result, TStepResultStatusEnum.success)
    except Exception as err:
        logger.error(f"执行ui操作失败\n {traceback.format_exc()}")
        runner.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        raise
    finally:
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
        runner.set_run_log(step_result=step_result, log_type=TStepLogType.end)


class RunUiStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_ui_request(runner, self.__step, **kwargs)
