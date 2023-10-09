# -*- coding: utf-8 -*-
# @author: xiao bai
import sys
import time
import traceback
from datetime import datetime

from zerorunner.model.result_model import StepResult
from zerorunner.model.step_model import TStep
from zerorunner.models import TStepResultStatusEnum


class TStepResult:

    def __init__(self, step: TStep, step_tag: str):
        self.result = StepResult(name=step.name,
                                 index=step.index,
                                 step_type=step.step_type,
                                 start_time=time.time(),
                                 step_tag=step_tag,
                                 )
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
            self.err_log(traceback.format_exc())

    def get_step_result(self):
        return self.result

    def set_step_log(self, message: str = None):
        """
        args :
            message: 日志内容
            log_type: 内容类型 start end  success fail skip err 等
        """
        if message:
            log_header = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:"
            self.result.log += f"{log_header}{message}\n"

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
