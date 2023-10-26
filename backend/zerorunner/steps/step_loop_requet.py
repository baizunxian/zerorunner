# -*- coding: utf-8 -*-
# @author: xiaobai

import time
import traceback
import typing

from loguru import logger

from zerorunner import exceptions
from zerorunner.models.base import TStepResultStatusEnum, LoopTypeEnum
from zerorunner.models.step_model import TStep
from zerorunner.parser import parse_string_to_json
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult


def run_loop_request(runner: SessionRunner,
                     step: TStep,
                     step_tag: str = None,
                     parent_step_result: TStepResult = None):
    """循环控制器"""
    step.name = "循环控制器"
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    # request_dict = step.loop_request.dict()
    # parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    # step.loop_request = TLoopRequest(**parsed_request_dict)
    try:
        # 次数循环
        if step.request.loop_type.lower() == LoopTypeEnum.Count.value:
            step_result.set_step_log("🔄次数循环---> 开始")
            for i in range(min(step.request.count_number, 100)):
                try:
                    runner.execute_loop(step.children_steps,
                                        step_tag=f"Loop {i + 1}",
                                        parent_step_result=step_result)
                    step_result.set_step_log(f"次数循环---> 第{i + 1}次")
                    time.sleep(step.request.count_sleep_time)
                except Exception as err:
                    logger.error(err)
                    continue
            step_result.set_step_log("次数循环---> 结束")

        # for 循环
        elif step.request.loop_type.lower() == LoopTypeEnum.For.value:
            for_variable_name = step.request.for_variable_name
            merge_variable = runner.get_merge_variable()
            iterable_obj = parse_string_to_json(step.request.for_variable)
            iterable_obj = runner.parser.parse_data(iterable_obj, merge_variable)
            if not isinstance(iterable_obj, typing.Iterable):
                step_result.set_step_log(f"for 循环错误： 变量 {iterable_obj} 不是一个可迭代对象！")
                raise ValueError("for 循环错误： 变量 {iterable_obj} 不是一个可迭代对象！")
            step_result.set_step_log("🔄for循环---> 开始")
            for for_variable_value in iterable_obj:
                try:
                    # 设置变量
                    runner.with_session_variables({for_variable_name: for_variable_value})
                    # 执行循环
                    runner.execute_loop(steps=step.children_steps,
                                        step_tag=f"For {for_variable_value}",
                                        parent_step_result=step_result)
                    time.sleep(step.request.for_sleep_time)
                except Exception as err:
                    logger.error(err)
                    continue
            step_result.set_step_log("🔄for循环---> 结束")

        # while 循环  最大循环次数 100
        elif step.request.loop_type.lower() == LoopTypeEnum.While.value:
            # todo 循环超时时间待实现
            run_number = 0
            step_result.set_step_log("🔄while循环---> 开始")
            step.request.while_value = parse_string_to_json(step.request.while_value)
            while True:
                while_variable = runner.parser.parse_data(step.request.while_variable,
                                                          runner.get_merge_variable(step))
                while_value = runner.parser.parse_data(step.request.while_value, runner.get_merge_variable(step))
                c_result = runner.comparators(while_variable,
                                              while_value,
                                              step.request.while_comparator)
                check_value = c_result.get("check_value", "")
                if c_result.get("check_result", "fail") == "success":
                    step_result.set_step_log(f"条件符合退出while循环 ---> {c_result}")
                    break
                step_result.set_step_log(f"条件不满足继续while循环 ---> {c_result}")
                try:
                    runner.execute_loop(steps=step.children_steps,
                                        step_tag=f"while {check_value}",
                                        parent_step_result=step_result)
                    step_result.set_step_result_status(TStepResultStatusEnum.success)
                except Exception as err:
                    # 执行for循环错误
                    step_result.set_step_log(f"执行for循环错误:{str(err)}")
                    logger.error(traceback.format_exc())
                    continue
                run_number += 1
                if run_number > 100:
                    step_result.set_step_log("循环次数大于100退出while循环")
                    break
                time.sleep(step.request.while_sleep_time or 1)
            step_result.set_step_log(f"🔄while循环---> 结束")
        else:
            raise exceptions.LoopNotFound("请确认循环类型是否为 count for while ")

        step_result.set_step_result_status(TStepResultStatusEnum.success)

    except Exception as exc:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise exc

    finally:
        step_result.end_log()
        step_result = step_result.get_step_result()
        if parent_step_result:
            parent_step_result.set_step_log_not_show_time(step_result.log)
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
        # 将数据平铺出来
        if step_result.step_result:
            for sub_step_result in step_result.step_result:
                runner.append_step_result(sub_step_result, parent_step_result=parent_step_result)
        step_result.step_result = []


class IFWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_check(self, check: typing.Any) -> "IFWithOptionalArgs":
        """校验变量"""
        self.__step.request.check = check
        return self

    def with_comparator(self, comparator: str) -> "IFWithOptionalArgs":
        """对比规则"""
        self.__step.request.comparator = comparator
        return self

    def with_expect(self, expect: typing.Any) -> "IFWithOptionalArgs":
        """对比值"""
        self.__step.request.expect = expect
        return self

    def with_remarks(self, remarks: str) -> "IFWithOptionalArgs":
        """对比值"""
        self.__step.request.remarks = remarks
        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def run(self, runner: SessionRunner, **kwargs):
        return run_loop_request(runner, self.__step, **kwargs)


class RunLoopStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_loop_request(runner, self.__step, **kwargs)
