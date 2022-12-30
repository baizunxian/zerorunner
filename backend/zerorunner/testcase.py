# -*- coding: utf-8 -*-
# @author: xiaobai
import copy
import unittest
from typing import List

from loguru import logger

from zerorunner import models, exceptions
from zerorunner.report import HtmlTestResult
from zerorunner import runner


class TestCase(unittest.TestCase):

    def __init__(self, runner: runner.Runner, teststep: models.TController):
        super(TestCase, self).__init__()
        self.runner = runner
        self.teststep = copy.copy(teststep)

    def runTest(self):
        """ 运行测试用例.
        """
        if self.runner.config.name:
            TestCase.__doc__ = self.runner.config.name
        try:
            self.runner.run_step(self.teststep)
        except exceptions.MyBaseFailure as ex:
            self.fail(str(ex))


# class TestSuite(unittest.TestSuite):
#     def __init__(self, test_suites: models.TestCase):
#         super(TestSuite, self).__init__()
#         for test_step in test_suites.teststeps:
#             self.__add_case_to_suite(test_step)
#
#     def __add_case_to_suite(self, test_step: models.TController):
#         test = TestCase(test_step)
#         self.addTest(test)


class ZeroRunner(object):
    def __init__(self, failfast: bool = False):
        self.exception_stage = "initialize HttpRunner()"
        kwargs = {"failfast": failfast, "resultclass": HtmlTestResult}
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self._summary = None

    def add_tests(self, testcase: models.TestCase) -> "unittest.TestSuite":

        test_suite = unittest.TestSuite()

        for test_step in testcase.teststeps:
            test_runner = runner.Runner()
            test_runner.with_config(testcase.config)
            testcase = TestCase(runner=test_runner, teststep=test_step)
            # suppose one testcase should not have more than 9999 steps,
            # and one step should not run more than 999 times.
            test_suite.addTest(testcase)

        return test_suite

    def _run_suite(self, test_suite: unittest.TestSuite):
        """run tests in test_suite

        Args:
            test_suite: unittest.TestSuite()

        Returns:
            list: tests_results

        """
        tests_results = []

        for testcase in test_suite:
            testcase_name = testcase.runner.config.name
            logger.info("Start to run testcase: {}".format(testcase_name))

            result = self.unittest_runner.run(testcase)
            if result.wasSuccessful():
                tests_results.append((testcase, result))
            else:
                tests_results.insert(0, (testcase, result))

        return tests_results

    def run_tests(self, tests_mapping):
        """run testcase/testsuite data"""


        # add tests to test suite
        self.exception_stage = "add tests to test suite"
        test_suite = self.add_tests(tests_mapping)

        # run test suite
        self.exception_stage = "run test suite"
        results = self._run_suite(test_suite)

        # aggregate results
        self.exception_stage = "aggregate results"
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
