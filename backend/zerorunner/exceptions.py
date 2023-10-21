# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

""" 标记失败的错误类型"""


class MyBaseFailure(Exception):
    pass


class ParseTestsFailure(MyBaseFailure):
    pass


class ValidationFailure(MyBaseFailure):
    pass


class ExtractFailure(MyBaseFailure):
    pass


class SetupHooksFailure(MyBaseFailure):
    pass


class TeardownHooksFailure(MyBaseFailure):
    pass


"""标记错误的错误类型"""


class MyBaseError(Exception):
    pass


class FileFormatError(MyBaseError):
    pass


class TestCaseFormatError(FileFormatError):
    pass


class TestSuiteFormatError(FileFormatError):
    pass


class ParamsError(MyBaseError):
    pass


class NotFoundError(MyBaseError):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class FunctionNotFound(NotFoundError):
    pass


class VariableNotFound(NotFoundError):
    pass


class EnvNotFound(NotFoundError):
    pass


class CSVNotFound(NotFoundError):
    pass


class ApiNotFound(NotFoundError):
    pass


class TestcaseNotFound(NotFoundError):
    pass


class SummaryEmpty(MyBaseError):
    """ test result summary data is empty
    """


class LoopNotFound(NotFoundError):
    pass


class StepRuntimeError(MyBaseError):
    """步骤运行错误"""
    pass


class EnvInitError(MyBaseError):
    """环境初始化失败"""
    pass
