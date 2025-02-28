# -*- coding: utf-8 -*-
# @author: xiao bai
import sys
import time
import traceback
from datetime import datetime

from zerorunner.models.result_model import StepResult
from zerorunner.models.step_model import TStep
from zerorunner.models.base import TStepResultStatusEnum


class TStepResult:

    def __init__(self, step: TStep, runner, step_tag: str):
        self.err_limit = 1
        self.result: StepResult = StepResult.parse_obj(step.dict())
        self.result.index = runner.get_step_run_index()
        self.result.start_time = time.time()
        self.result.step_tag = step_tag
        if hasattr(step, "case_id"):
            self.result.case_id = step.case_id

    def set_step_result_status(self, status: TStepResultStatusEnum, msg: str = ""):
        """设置步骤状态"""

        self.result.message = msg
        _, exc_value, _ = sys.exc_info()

        if status == TStepResultStatusEnum.success:
            self.result.success = True
            self.result.status = TStepResultStatusEnum.success.value
            self.success_log(msg)

        if status == TStepResultStatusEnum.fail:
            self.result.success = False
            self.result.status = TStepResultStatusEnum.fail.value
            self.result.message = msg if msg else str(exc_value)
            self.fail_log(traceback.format_exc())

        if status == TStepResultStatusEnum.skip:
            self.result.success = True
            self.result.status = TStepResultStatusEnum.skip.value
            # self.result.message = msg if msg else "跳过"
            self.skip_log(msg)

        if status == TStepResultStatusEnum.err:
            self.result.success = False
            self.result.status = TStepResultStatusEnum.err.value
            self.result.message = msg if msg else str(exc_value)
            self.err_log(traceback.format_exc(limit=self.err_limit))

    def get_step_result(self):
        return self.result

    def set_step_log(self, message: str = None, show_time: bool = True):
        """
        args :
            message: 日志内容
            log_type: 内容类型 start end  success fail skip err 等
        """
        if message:
            message = message if message.endswith('\n') else message + '\n'
            self.result.log += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':' if show_time else ''}{message}"

    def set_step_log_not_show_time(self, message):
        """设置日志，不在日志前加时间"""
        if message:
            message = message if message.endswith('\n') else message + '\n'
            self.result.log += message

    def start_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: ▶️开始{new_msg}")

    def end_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: ⏹️结束{new_msg}")

    def success_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 🎉成功~{new_msg}")

    def fail_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 😅 失败~{new_msg}")

    def skip_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 🪂 跳过~{new_msg}")

    def wait_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 🪂 等待~{new_msg}")

    def loop_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 🔄 循环~{new_msg}")

    def if_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 🔀 条件~{new_msg}")

    def err_log(self, message: str = None):
        new_msg = f"\n{message}" if message else ""
        self.set_step_log(f"{self.result.name}: 💣 错误~{new_msg}")
