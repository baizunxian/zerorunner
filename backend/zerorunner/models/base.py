# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from enum import Enum

from pydantic import HttpUrl

Name = str
Url = str
BaseUrl = typing.Union[HttpUrl, str]
VariablesMapping = typing.Dict[str, typing.Any]
ParametersMapping = typing.Dict[str, typing.Any]
FunctionsMapping = typing.Dict[str, typing.Callable]
Headers = typing.Dict[str, str]
Cookies = typing.Dict[str, str]
Verify = bool
Hooks = typing.List[typing.Any]
Export = typing.List[str]
Validators = typing.List[typing.Dict]
Env = typing.Dict[str, typing.Any]


class MethodEnum(str, Enum):
    """请求方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    NA = "N/A"


class TStepTypeEnum(str, Enum):
    """步骤类型枚举"""
    api = "api"
    case = "case"
    wait = "wait"
    script = "script"
    sql = "sql"
    extract = "extract"
    loop = "loop"
    IF = "IF"
    ui = "ui"


TStepControllerDict = {
    "api": "接口",
    "case": "用例",
    "wait": "等待控制器",
    "db_script": "脚本控制器",
    "sql": "sql控制器",
    "extract": "提取控制器",
    "loop": "循环控制器",
    "if": "条件控制器",
    "ui": "ui用例"
}


class LoopTypeEnum(str, Enum):
    """循环类型枚举"""
    For = "for"
    Count = "count"
    While = "while"


class ComparatorEnum(str, Enum):
    """比较方法枚举， 条件控制器， 循环控制 使用"""
    equals = "equals"
    not_equals = "not_equals"
    contains = "contains"
    not_contains = "not_contains"
    gt = "gt"
    lt = "lt"
    none = "none"
    not_none = "not_none"


class TStepResultStatusEnum(str, Enum):
    """步骤数据状态"""
    success = "SUCCESS"
    fail = "FAILURE"
    skip = "SKIP"
    err = "ERROR"


class TStepLogType(str, Enum):
    """步骤日志类型"""
    start = "开始"
    end = "结束"
    success = "成功"
    fail = "失败"
    skip = "跳过"
    err = "错误"
    wait = "等待"
    loop = "循环"
    condition = "条件"


class CheckModeEnum(str, Enum):
    """校验模式枚举"""
    JsonPath = "JsonPath"
    jmespath = "jmespath"
    variable_or_func = "variable_or_func"
    RequestHeaders = "request_headers"
    ResponseHeaders = "response_headers"


class ExtractTypeEnum(str, Enum):
    """提取类型枚举"""
    JsonPath = "JsonPath"
    jmespath = "jmespath"
    variable_or_func = "variable_or_func"
    RequestHeaders = "request_headers"
    ResponseHeaders = "response_headers"
