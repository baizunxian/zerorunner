# -*- coding: utf-8 -*-
# @author: xiaobai

import time
import traceback

from loguru import logger
from zerorunner.models.base import TStepLogType, TStepResultStatusEnum
from zerorunner.models.result_model import StepResult, UiSessionData
from zerorunner.models.step_model import TStep, TUiRequest
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.ext.zero_driver.keywords.web import WebAction
from zerorunner.steps.step_result import TStepResult


def run_ui_request(runner: SessionRunner,
                   step: TStep,
                   step_tag: str = None,
                   parent_step_result: TStepResult = None):
    """运行ui request"""
    # 清空step result 避免获取结果时出错
    runner.clear_step_results()
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    step_result.session_data = UiSessionData()
    step_result.session_data.action = step.request.action
    step_result.session_data.location_value = step.request.location_value
    step_result.session_data.location_method = step.request.location_method
    step_result.session_data.data = step.request.data

    start_time = time.time()
    try:
        step.variables.update(runner.zero_driver.get_session_variables())
        step_variables = runner.get_merge_variable(step)
        request_dict = step.request.dict()
        parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
        ui_step = TUiRequest.parse_obj(parsed_request_dict)
        if not hasattr(WebAction, ui_step.action):
            logger.error(f"操作方法不存在： {ui_step.action}")
            raise AttributeError(f"操作方法不存在： {ui_step.action}")
        getattr(WebAction, ui_step.action)(runner.zero_driver, ui_step)
        # 截图
        step_result.session_data.screenshot_file_base64 = runner.zero_driver.get_screenshot()
        step_result.set_step_result_status(TStepResultStatusEnum.success)
    except Exception as err:
        logger.error(f"执行ui操作失败\n {traceback.format_exc()}")
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise
    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        if parent_step_result:
            parent_step_result.set_step_log_not_show_time(step_result.log)
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)


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
