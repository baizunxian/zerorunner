# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from zerorunner.models.step_model import TStep, TRequest
from zerorunner.runner import SessionRunner
from zerorunner.steps.step_api_requet import RunRequestStep, StepRequestValidation, StepRequestExtraction, \
    RequestWithOptionalArgs
from zerorunner.steps.step_if_requet import RunIFStep
from zerorunner.steps.step_loop_requet import RunLoopStep
from zerorunner.steps.step_script_requet import RunScriptStep
from zerorunner.steps.step_sql_request import RunSqlStep
from zerorunner.steps.step_ui_requet import RunUiStep
from zerorunner.steps.step_wait_requet import RunWaitStep


class Step(object):
    def __init__(
            self,
            step: typing.Union[
                RunRequestStep,
                RunSqlStep,
                RunWaitStep,
                RunIFStep,
                RunLoopStep,
                RunScriptStep,
                StepRequestValidation,
                StepRequestExtraction,
                RequestWithOptionalArgs,
                RunUiStep,
            ],
    ):
        self.__step = step

    @property
    def request(self) -> TRequest:
        return self.__step.struct().request

    @property
    def retry_times(self) -> int:
        return self.__step.struct().retry_times

    @property
    def retry_interval(self) -> int:
        return self.__step.struct().retry_interval

    def struct(self) -> TStep:
        return self.__step.struct()

    def set_index(self, index):
        self.__step.struct().index = index

    def get_index(self):
        return self.__step.struct().index

    @property
    def name(self) -> str:
        return self.__step.name()

    def type(self) -> str:
        return self.__step.type()

    def run(self, runner: SessionRunner, **kwargs):
        return self.__step.run(runner, **kwargs)
