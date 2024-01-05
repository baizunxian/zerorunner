# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import sys
import time
import traceback
import typing
import uuid
from datetime import datetime
from unittest import SkipTest

from loguru import logger

from zerorunner import exceptions
from zerorunner.client import HttpSession
from zerorunner.exceptions import ValidationFailure
from zerorunner.ext.zero_driver.driver import ZeroDriver
from zerorunner.models.base import VariablesMapping, FunctionsMapping
from zerorunner.models.result_model import StepResult, TestCaseSummary, TestCaseInOut
from zerorunner.models.step_model import TStep, TConfig
from zerorunner.parser import parse_data, get_mapping_function, \
    Parser, parse_variables_mapping
from zerorunner.response import uniform_validator
from zerorunner.steps.step_result import TStepResult
from zerorunner.utils import merge_variables


class SessionRunner(object):
    config: TConfig
    teststeps: typing.List[typing.Any]

    parser: Parser = None
    case_id: str = ""
    extracted_variables: VariablesMapping = {}
    session: HttpSession = None
    # 错误信息或备注等信息记录
    message: str = ""

    __teststeps: typing.List[typing.Any]
    __export: typing.List[str] = []
    __step_results: typing.List[StepResult] = []
    __session_variables: VariablesMapping = {}
    __merge_variable_pool: VariablesMapping = {}
    __step_run_index = 0
    # time
    __start_time: float = 0
    __duration: float = 0
    # ui 驱动
    zero_driver: ZeroDriver = None
    # log
    __log__: str = ""

    def __init(self):
        self.__config = self.config
        self.__session_variables = self.__session_variables or {}
        self.__merge_variable_pool = self.__merge_variable_pool or {}
        self.extracted_variables = self.extracted_variables or {}
        self.__start_at = 0
        self.__duration = 0

        self.case_id = self.config.case_id or str(uuid.uuid4())
        self.__step_results = []
        self.session = HttpSession()
        self.parser = self.parser or Parser(self.config.functions)

    def with_config(self, config: TConfig) -> "SessionRunner":
        self.config = config
        return self

    def with_functions(self, function_map: FunctionsMapping) -> "SessionRunner":
        self.config.functions.update(function_map)
        return self

    def with_session(self, session: HttpSession) -> "SessionRunner":
        self.session = session
        return self

    def with_case_id(self, case_id: typing.Union[str, int]) -> "SessionRunner":
        self.case_id = case_id
        return self

    def with_session_variables(self, variables: VariablesMapping, cover=False) -> "SessionRunner":
        if cover:
            self.__session_variables = variables
        else:
            self.__session_variables.update(variables)
        return self

    def with_export(self, export: typing.List[str]) -> "SessionRunner":
        self.__export = export
        return self

    def get_session_variables(self):
        return self.__session_variables

    def append_step_result(self, step_result: StepResult, step_tag: str = None, parent_step_result: TStepResult = None):
        """setup_hooks teardown_hooks"""
        if parent_step_result:
            if step_tag and step_tag == "setup_hooks":
                parent_step_result.get_step_result().setup_hook_results.append(step_result)
            elif step_tag and step_tag == "teardown_hooks":
                parent_step_result.get_step_result().teardown_hook_results.append(step_result)
            else:
                parent_step_result.get_step_result().step_result.append(step_result)
        else:
            self.__step_results.append(step_result)

    @staticmethod
    def get_step_result(step: TStep, step_tag: str = None) -> StepResult:
        """步初始化骤结果对象"""
        step_result = StepResult(name=step.name,
                                 index=step.index,
                                 step_type=step.step_type,
                                 start_time=time.time(),
                                 step_tag=step_tag,
                                 )
        if hasattr(step, "case_id"):
            step_result.case_id = step.case_id
        return step_result

    def comparators(self, check: str, expect: str, comparator: str) -> typing.Dict[str, typing.Any]:
        """
        结果比较
        """
        merge_variable = self.get_merge_variable()

        check_value = parse_data(check, merge_variable, self.config.functions)
        expect_value = parse_data(expect, merge_variable, self.config.functions)
        u_validator = uniform_validator({"check": check_value, "expect": expect_value, "comparator": comparator})
        assert_method = u_validator["assert"]
        assert_func = get_mapping_function(assert_method, self.config.functions)
        validator_dict = {
            "comparator": assert_method,
            "check": check,
            "check_value": check_value,
            "expect": expect,
            "expect_value": expect_value,
            "check_result": "fail",
            "validate_msg": ""
        }
        try:
            assert_func(check_value, expect_value)
            validator_dict["check_result"] = "success"
        except AssertionError as ex:
            validator_dict["check_result"] = "fail"
            validate_msg = ""
            validate_msg += "\t==> fail"
            validate_msg += (
                f"\n"
                f"check_item: {check}\n"
                f"check_value: {check_value}({type(check_value).__name__})\n"
                f"assert_method: {assert_method}\n"
                f"expect_value: {expect_value}({type(expect_value).__name__})"
            )
            validator_dict["validate_msg"] = validate_msg

        return validator_dict

    def get_merge_variable_pool(self):
        return self.__merge_variable_pool

    def get_merge_variable(self, step: TStep = None, variables_mapping: VariablesMapping = None):
        """
        获取合并的变量
        优先级
        step.variables(用例变量) >
         __session_variables(会话变量) >
        extracted_variables(提取变量) >
        config.variables(用例变量) >
        config.env_variables(环境变量)>
        merge_variable_pool(合并后的变量池)
        """
        merge_variable_pool = merge_variables(self.config.env_variables, self.__merge_variable_pool)
        # 合并用例变量
        merge_variable_pool = merge_variables(self.config.variables, merge_variable_pool)
        # 合并提取变量
        merge_variable_pool = merge_variables(self.extracted_variables, merge_variable_pool)
        # 合并会话变量
        merge_variable_pool = merge_variables(self.__session_variables, merge_variable_pool)
        # 合并用例变量
        merge_variable_pool = merge_variables(self.__session_variables, merge_variable_pool)
        # 合并用例变量
        if step:
            merge_variable_pool = merge_variables(step.variables, merge_variable_pool)
        if variables_mapping:
            merge_variable_pool = merge_variables(variables_mapping, merge_variable_pool)
        merge_variable_pool = parse_variables_mapping(
            merge_variable_pool, self.parser.functions_mapping
        )
        self.__merge_variable_pool = merge_variable_pool
        return self.__merge_variable_pool

    def __parse_config(self, param: typing.Dict = None):
        """解析配置"""
        # parse config variables
        self.__config.variables.update(self.__session_variables)
        if param:
            self.__config.variables.update(param)
        self.__config.variables = self.parser.parse_variables(self.__config.variables)

        # parse config name
        self.__config.name = self.parser.parse_data(
            self.__config.name, self.__config.variables
        )

        # parse config base url
        self.__config.base_url = self.parser.parse_data(
            self.__config.base_url, self.__config.variables
        )

    def get_step_results(self) -> typing.List[StepResult]:
        """获取步骤"""
        return self.__step_results

    def clear_step_results(self):
        """清空步骤结果"""
        self.__step_results.clear()

    def handle_skip_feature(self, step: TStep):
        """ handle skip feature for testcase
            - skip: skip current test unconditionally
            - skipIf: skip current test if condition is true
            - skipUnless: skip current test unless condition is true
        """
        skip_reason = None
        if skip_reason:
            raise SkipTest(skip_reason)

    def get_export_variables(self) -> typing.Dict:
        """获取导出的变量"""
        # override testcase export vars with step export
        export_var_names = self.__export or self.config.export
        export_vars_mapping = {}
        for var_name in export_var_names:
            if var_name not in self.__session_variables:
                raise exceptions.ParamsError(
                    f"failed to export variable {var_name} from session variables {self.__session_variables}"
                )

            export_vars_mapping[var_name] = self.__session_variables[var_name]

        return export_vars_mapping

    def get_step_run_index(self):
        return self.__step_run_index

    def get_summary(self) -> TestCaseSummary:
        """获取测试用例结果摘要"""
        start_at_timestamp = self.__start_time
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()

        summary_success = True
        for step_result in self.__step_results:
            if not step_result.success:
                summary_success = False
                break

        testcase_summary = TestCaseSummary(
            name=self.config.name,
            success=summary_success,
            message=self.message,
            case_id=self.config.case_id,
            start_time=self.__start_time,
            start_time_iso_format=start_at_iso_format,
            duration=round(self.__duration, 3),
            in_out=TestCaseInOut(
                config_vars=self.config.variables,
                # export_vars=self.get_export_variables(),
            ),
            log=self.__log__,
            step_results=self.__step_results,
        )
        return testcase_summary

    def run_step(self, step, step_tag: str = None, parent_step_result: TStepResult = None):
        """运行步骤，可以运行实现IStep run 方法的任何步骤
        Args:
            step (Step): obj IStep
            step_tag (str): 步骤标签
            parent_step_result (StepResult): 父级结构
        """
        self.__init()
        # run step
        logger.info(f"run step begin: {step.name} >>>>>>")
        if not self.__start_time:
            self.__start_time = time.time()
        for i in range(step.retry_times + 1):
            try:
                self.__step_run_index += 1
                step.run(self, step_tag=step_tag, parent_step_result=parent_step_result)
            except ValidationFailure:
                if i == step.retry_times:
                    raise
                else:
                    logger.warning(
                        f"运行步骤 {step.name()} 校验失败,等待 {step.retry_interval} 秒后重试"
                    )
                    time.sleep(step.retry_interval)
                    logger.info(
                        f"运行步骤重试 ({i + 1}/{step.retry_times} time): {step.name()} >>>>>>"
                    )
            except Exception:
                logger.error(f"步骤执行错误:\n{traceback.format_exc()}")

        logger.info(f"run step end: {step.name} <<<<<<\n")

    def execute_loop(self,
                     steps: typing.List[object],
                     step_tag=None,
                     parent_step_result: TStepResult = None):
        """
        执行循环
        :param steps: 步骤
        :param step_tag: 步骤标签
        :param parent_step_result: 父级步骤结果
        :return:
        """
        for step in steps:
            if hasattr(step, "set_index") and hasattr(step, "get_index"):
                step.set_index(step.get_index() + 1)
            self.run_step(step, step_tag=step_tag, parent_step_result=parent_step_result)

    def test_start(self, param: typing.Dict = None) -> "SessionRunner":
        """
        开始测试
        :param param: 参数
        :return:
        """
        self.__init()
        self.__parse_config(param)
        self.case_id = self.case_id or str(uuid.uuid4())
        log_handler = logger.add(sys.stdin, level="INFO")
        logger.info(
            f"Start to run testcase: {self.config.name}, TestCase ID: {self.case_id}"
        )

        try:
            for step in self.teststeps:
                self.run_step(step)

        finally:
            logger.remove(log_handler)
        return self
