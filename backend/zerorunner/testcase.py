# -*- coding: utf-8 -*-
# @author: xiaobai
import copy
import unittest
from typing import List

from loguru import logger

from zerorunner import models, exceptions
from zerorunner.report import HtmlTestResult
from zerorunner import runner


class ZeroRunner(object):
    def __init__(self, failfast: bool = False):
        self.exception_stage = "initialize HttpRunner()"
        kwargs = {"failfast": failfast, "resultclass": HtmlTestResult}
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self._summary = None

    def add_tests(self, testcase: models.TestCase) -> "unittest.TestSuite":

        def _add_test(test_runner: runner.Runner, test_step: models.TController):
            """
            test_runner : Runner
            test_step : TController
            """

            def test(self):
                try:
                    test_runner.run_testcase(test_step)
                except exceptions.MyBaseFailure as ex:
                    self.fail(str(ex))
                finally:
                    self.summary = test_runner.get_summary()

            test.__doc__ = test_step.name

            return test

        test_suite = unittest.TestSuite()

        for index, step in enumerate(testcase.teststeps):
            test_runner = runner.Runner()
            test_runner.with_config(testcase.config)
            test_method_name = "test_{:04}".format(index)
            test_method = _add_test(test_runner, step)

            TestSequence = type("TestSequence", (unittest.TestCase,), {})

            setattr(TestSequence, test_method_name, test_method)

            loaded_testcase = self.test_loader.loadTestsFromTestCase(TestSequence)

            setattr(loaded_testcase, "config", testcase.config)
            setattr(loaded_testcase, "teststeps", testcase.teststeps)
            setattr(loaded_testcase, "runner", test_runner)
            test_suite.addTest(loaded_testcase)

        return test_suite

    def _run_suite(self, test_suite: unittest.TestSuite) -> List:
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
            if result.wasSuccessful():
                tests_results.append((testcase, result))
            else:
                tests_results.insert(0, (testcase, result))

        return tests_results

    def run_tests(self, testcase: models.TestCase):
        """run testcase/testsuite data"""

        # add tests to test suite
        self.exception_stage = "添加用例到套件"
        test_suite = self.add_tests(testcase)

        # run test suite
        self.exception_stage = "运行测试套件"
        results = self._run_suite(test_suite)

        # aggregate results
        self.exception_stage = "汇总结果"
        # self._summary = self._aggregate(results)
        #
        # # generate html report
        # self.exception_stage = "generate html report"
        # report.stringify_summary(self._summary)
        #
        # if self.save_tests:
        #     utils.dump_logs(self._summary, project_mapping, "summary")
        #     # save variables and export data
        #     vars_out = self.get_vars_out()
        #     utils.dump_logs(vars_out, project_mapping, "io")

        return self._summary

    def _aggregate(self, tests_results):
        """aggregate results

        Args:
            tests_results (list): list of (testcase, result)

        """
        summary = {
            "success": True,
            "stat": {
                "testcases": {"total": len(tests_results), "success": 0, "fail": 0},
                "teststeps": {},
            },
            "time": {},
            "details": [],
        }

        for tests_result in tests_results:
            testcase, result = tests_result
            testcase_summary = report.get_summary(result)

            if testcase_summary["success"]:
                summary["stat"]["testcases"]["success"] += 1
            else:
                summary["stat"]["testcases"]["fail"] += 1

            summary["success"] &= testcase_summary["success"]
            testcase_summary["name"] = testcase.config.get("name")
            testcase_summary["in_out"] = utils.get_testcase_io(testcase)

            report.aggregate_stat(
                summary["stat"]["teststeps"], testcase_summary["stat"]
            )
            report.aggregate_stat(summary["time"], testcase_summary["time"])

            summary["details"].append(testcase_summary)

        return summary
