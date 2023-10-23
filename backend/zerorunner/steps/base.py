# -*- coding: utf-8 -*-
# @author: xiaobai
from zerorunner.models.step_model import TStep


class IStep(object):
    """步骤基类"""

    def name(self) -> str:
        raise NotImplementedError

    def type(self) -> str:
        raise NotImplementedError

    def struct(self) -> TStep:
        raise NotImplementedError

    def run(self, runner, **kwargs):
        # runner: SessionRunner
        raise
