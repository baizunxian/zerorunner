# encoding: utf-8
import time
import unittest

from loguru import logger


class HtmlTestResult(unittest.TextTestResult):
    """A html result class that can generate formatted html results.

    Used by TextTestRunner.
    """

    def __init__(self, stream, descriptions, verbosity):
        super(HtmlTestResult, self).__init__(stream, descriptions, verbosity)
        self.summary = None

    def _record_test(self, test, status, attachment=''):
        # test_summary: TestCaseSummary = test.summary
        # if test_summary.step_results:
        #     test_summary.step_results[-1].status = status.upper()
        #     # test_summary.step_results[-1].message = attachment
        #     test_summary.step_results[-1].success = True if status == "success" else False
        self.summary = test.summary

    def startTestRun(self):
        self.start_at = time.time()

    def startTest(self, test):
        """ add start test time """
        super(HtmlTestResult, self).startTest(test)
        logger.info(test.shortDescription(), "yellow")

    def addSuccess(self, test):
        super(HtmlTestResult, self).addSuccess(test)
        self._record_test(test, 'success')
        print("")

    def addError(self, test, err):
        super(HtmlTestResult, self).addError(test, err)
        self._record_test(test, 'error', self._exc_info_to_string(err, test))
        print("")

    def addFailure(self, test, err):
        super(HtmlTestResult, self).addFailure(test, err)
        self._record_test(test, 'failure', self._exc_info_to_string(err, test))
        print("")

    def addSkip(self, test, reason):
        super(HtmlTestResult, self).addSkip(test, reason)
        self._record_test(test, 'skip', reason)
        print("")

    def addExpectedFailure(self, test, err):
        super(HtmlTestResult, self).addExpectedFailure(test, err)
        self._record_test(test, 'ExpectedFailure', self._exc_info_to_string(err, test))
        print("")

    def addUnexpectedSuccess(self, test):
        super(HtmlTestResult, self).addUnexpectedSuccess(test)
        self._record_test(test, 'UnexpectedSuccess')
        print("")

    @property
    def duration(self):
        return time.time() - self.start_at
