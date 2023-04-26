# -*- coding: utf-8 -*-
# @author: xiaobai

import time
import typing
from zerorunner import exceptions
from zerorunner.model.base import TStepLogType, TStepResultStatusEnum
from zerorunner.model.result_model import StepResult
from zerorunner.model.step_model import TStep, TIFRequest
from zerorunner.runner_new import SessionRunner
from zerorunner.steps.base import IStep


def run_if_request(runner: SessionRunner,
                   step: TStep,
                   step_tag: str = None,
                   parent_step_result: StepResult = None):
    """条件控制器"""
    step.name = "条件控制器"
    step_result = runner.get_step_result(step, step_tag)
    runner.set_run_log(step_result=step_result, log_type=TStepLogType.start)
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.if_request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    try:
        if_request_obj = TIFRequest(**parsed_request_dict)
        if not if_request_obj.comparator:
            raise ValueError("条件控制器--> 条件不能为空！")
        c_result = runner.comparators(if_request_obj.check, if_request_obj.expect, if_request_obj.comparator)
        check_value = c_result.get("check_value", "")
        if c_result.get("check_result", "fail") != "success":
            runner.set_run_log(f"条件不符---> {c_result.get('validate_msg', '')}")
            raise exceptions.ValidationFailure(f"条件不符---> {c_result.get('validate_msg', '')}")
        try:
            runner.execute_loop(if_request_obj.teststeps, step_tag=f"IF {check_value}", parent_step_result=step_result)
        except Exception as err:
            raise

        runner.set_step_result_status(step_result, TStepResultStatusEnum.success)
    except exceptions.VariableNotFound as err:
        runner.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        raise
    except Exception as err:
        runner.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        raise

    finally:
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
        # 将数据平铺出来
        if step_result.step_result:
            for sub_step_result in step_result.step_result:
                runner.append_step_result(sub_step_result)
        step_result.step_result = []
        runner.set_run_log(step_result=step_result, log_type=TStepLogType.end)


class IFWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_check(self, check: typing.Any) -> "IFWithOptionalArgs":
        """校验变量"""
        self.__step.if_request.check = check
        return self

    def with_comparator(self, comparator: str) -> "IFWithOptionalArgs":
        """对比规则"""
        self.__step.if_request.comparator = comparator
        return self

    def with_expect(self, expect: typing.Any) -> "IFWithOptionalArgs":
        """对比值"""
        self.__step.if_request.expect = expect
        return self

    def with_remarks(self, remarks: str) -> "IFWithOptionalArgs":
        """对比值"""
        self.__step.if_request.remarks = remarks
        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def run(self, runner: SessionRunner, **kwargs):
        return run_if_request(runner, self.__step, **kwargs)


class RunIFStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_if_request(runner, self.__step, **kwargs)
