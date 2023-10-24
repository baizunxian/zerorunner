# -*- coding: utf-8 -*-
# @author: xiaobai
import time
import typing
import unittest
import uuid

from loguru import logger

from autotest.utils.async_converter import AsyncIOPool
from zerorunner import exceptions
from zerorunner.models import step_model
from zerorunner.models.result_model import TestCaseSummary
from zerorunner.parser import Parser
from zerorunner.reports import HtmlTestResult
from zerorunner.runner import SessionRunner
from zerorunner.report.stringify import stringify_summary
from zerorunner.steps.step import Step


class ZeroRunner(object):
    def __init__(self, failfast: bool = False, session_runner: SessionRunner = None):
        self.exception_stage = "initialize ZeroRunner()"
        kwargs = {"failfast": failfast, "resultclass": HtmlTestResult, "verbosity": 0}
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self._summary = None
        self.report_id = None
        self.session_runner = session_runner

    def add_tests(self, testcase: step_model.TestCase) -> typing.List[unittest.TestSuite]:

        def _add_test(test_runner: SessionRunner, test_step: Step):
            """
            test_runner : Runner
            test_step : TController
            """

            def test(self):
                try:
                    test_runner.run_step(test_step)
                except exceptions.MyBaseFailure as ex:
                    self.fail(str(ex))
                finally:
                    self.summary = test_runner.get_summary()

            test.__doc__ = test_step.name if test_step.name else str(uuid.uuid4())

            return test

        # test_suite = unittest.TestSuite()
        testcase_list = []

        # 用例依赖时公用一个 SessionRunner 获取提交变量等数据
        if testcase.config.step_rely and not self.session_runner:
            self.session_runner = SessionRunner()

        for index, step in enumerate(testcase.teststeps):
            test_runner = self.session_runner if self.session_runner else SessionRunner()
            test_runner.with_config(testcase.config)
            test_method_name = "test_{:04}".format(index)
            test_method = _add_test(test_runner, step)

            TestSequence = type("TestSequence", (unittest.TestCase,), {})

            setattr(TestSequence, test_method_name, test_method)

            loaded_testcase = self.test_loader.loadTestsFromTestCase(TestSequence)

            setattr(loaded_testcase, "config", testcase.config)
            setattr(loaded_testcase, "teststeps", testcase.teststeps)
            setattr(loaded_testcase, "runner", test_runner)
            testcase_list.append(loaded_testcase)
            # test_suite.addTest(loaded_testcase)

        return testcase_list

    def add_suite(self, testcase_list: typing.List[unittest.TestSuite]) -> "unittest.TestSuite":
        test_suite = unittest.TestSuite()
        test_suite.addTests(testcase_list)
        return test_suite

    def _run_suite(self, test_suite: unittest.TestSuite) -> typing.List:
        """run tests in test_suite

        Args:
            test_suite: unittest.TestSuite()

        Returns:
            list: tests_results

        """
        tests_results = []

        for testcase in test_suite:
            testcase_name = testcase.config.name
            logger.info(f"开始运行测试用例: {testcase_name}")

            result = self.unittest_runner.run(testcase)
            # if result.wasSuccessful():
            tests_results.append((testcase, result))
            # else:
            #     tests_results.insert(0, (testcase, result))

        return tests_results

    def run_tests(self, testcase: step_model.TestCase):
        """run testcase/testsuite data"""

        self.exception_stage = "添加用例到套件"
        testcase_list = self.add_tests(testcase)
        test_suite = self.add_suite(testcase_list)

        self.exception_stage = "运行测试套件"
        results = self._run_suite(test_suite)

        self.exception_stage = "汇总结果"
        self._summary = self._aggregate(results)
        stringify_summary(self._summary)

        return self._summary

    def _aggregate(self, tests_results):
        """aggregate results

        Args:
            tests_results (list): list of (testcase, result)

        """

        summary = TestCaseSummary(name="", success=True, case_id=None)

        for index, tests_result in enumerate(tests_results):
            testcase, result = tests_result
            testcase_summary: TestCaseSummary = result.summary
            if index == 0:
                summary.start_time = testcase_summary.start_time
                summary.start_time_iso_format = testcase_summary.start_time_iso_format
            summary.name = testcase_summary.name
            summary.case_id = testcase_summary.case_id
            summary.in_out = testcase_summary.in_out
            summary.log += f"\n{testcase_summary.log}"
            summary.run_count += 1
            for step in testcase_summary.step_results:
                summary.actual_run_count += 1
                step_status = step.status.lower()
                if step_status == "success":
                    summary.run_success_count += 1
                elif step_status == "fail":
                    summary.run_fail_count += 1
                elif step_status == "error":
                    summary.run_err_count += 1
                elif step_status == "skip":
                    summary.run_skip_count += 1
                step.duration = round(step.duration, 3)
                summary.duration += step.duration
                summary.step_results.append(step)
            for step in testcase_summary.step_results:
                if not step.success:
                    summary.success = False
                    break
        summary.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(summary.start_time))
        return summary
