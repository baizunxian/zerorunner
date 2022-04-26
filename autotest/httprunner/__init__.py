__version__ = "3.1.11"
__description__ = "One-stop solution for HTTP(S) testing."

# import firstly for monkey patch if needed

from autotest.httprunner.parser import parse_parameters as Parameters
from autotest.httprunner.runner import HttpRunner
from autotest.httprunner.testcase import Config, Step, RunRequest, RunTestCase

__all__ = [
    "__version__",
    "__description__",
    "HttpRunner",
    "Config",
    "Step",
    "RunRequest",
    "RunTestCase",
    "Parameters",
]
