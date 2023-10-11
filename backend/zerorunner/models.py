# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import typing
from enum import Enum

from pydantic import BaseModel, Field
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
# Hooks = typing.List[Union[Text, Dict[Text, Text]]]
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


class TStepControllerEnum(str, Enum):
    """步骤类型枚举"""
    api = "api"
    case = "case"
    wait = "wait"
    script = "db_script"
    sql = "sql"
    extract = "extract"
    loop = "loop"
    IF = "IF"


TStepControllerDict = {
    "api": "接口",
    "case": "用例",
    "wait": "等待控制器",
    "db_script": "脚本控制器",
    "sql": "sql控制器",
    "extract": "提取控制器",
    "loop": "循环控制器",
    "if": "条件控制器"
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
    start = "开始"
    end = "结束"
    success = "成功"
    fail = "失败"
    skip = "跳过"
    err = "错误"
    wait = "等待"
    loop = "循环"
    condition = "条件"


class TStepTagEnum(str, Enum):
    pre = "pre"  # 前置
    post = "post"  # 后置
    controller = "controller"  # 控制器


class TConfig(BaseModel):
    case_id: typing.Union[str, int, None] = None
    name: Name
    verify: Verify = False
    verify: Verify = False
    base_url: BaseUrl = ""
    # 脚本函数
    functions: FunctionsMapping = {}  # TestCase 脚本函数
    # 环境变量
    env_variables: typing.Union[VariablesMapping, str] = {}
    # 请求头
    headers: VariablesMapping = {}
    # 配置变量
    variables: typing.Union[VariablesMapping, str] = {}
    # 参数
    parameters: typing.Union[VariablesMapping, str] = {}
    # setup_hooks: Hooks = []
    # teardown_hooks: Hooks = []
    export: Export = []
    # path: str = None
    weight: int = 1


class TRequest(BaseModel):
    """请求模型"""
    method: MethodEnum
    url: Url
    params: typing.Dict[str, str] = {}
    headers: Headers = {}
    req_json: typing.Union[typing.Dict, typing.List, str] = Field(None, alias="json")
    data: typing.Union[str, typing.Dict[str, typing.Any]] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: typing.Dict = {}  # used for upload files


class TBaseController(BaseModel):
    name: Name = ""
    value: typing.Any = ""
    enable: bool = True  # 是否有效
    index: int = 0  # 顺序
    step_id: str = None  # 唯一步骤id
    parent_step_id: str = None  # 父级id  step_id


class ExtractData(BaseModel):
    name: str = ""
    path: str = ""
    continue_extract = False
    continue_index: int = 0
    extract_type: str = ""  # 提取类型  jmespath


class TApiController(TBaseController):
    case_id: typing.Union[str, int] = ''
    step_type: typing.Literal['api'] = "api"
    request: typing.Union[TRequest, None] = None
    testcase: typing.Union[str, typing.Callable, None] = None
    variables: VariablesMapping = {}
    # parameters 加入步骤 参数
    parameters: ParametersMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    message: str = ''
    # used to extract request's response field
    extracts: typing.List[ExtractData] = []
    # used to export session variables from referenced testcase
    export: Export = []
    validators: Validators = Field([], alias="validate")


class TScriptController(TBaseController):
    """脚本控制"""
    value: typing.Optional[str] = None
    step_type: typing.Literal["db_script"]


class TWaitController(TBaseController):
    """等待控制器"""
    step_type: typing.Literal["wait"]
    value: typing.Optional[int] = None


class TIFController(TBaseController):
    step_type: typing.Literal["if"]
    check: str = ""  # 校验变量
    comparator: str = ""  # 对比规则
    expect: str = ""  # 对比值
    remarks: str = ""  # 备注
    teststeps: typing.List["TController"] = []


class TLoopController(TBaseController):
    """循环控制器"""
    step_type: typing.Literal["loop"]
    teststeps: typing.List["TController"] = []
    loop_type: typing.Literal["count", "for", "while"]
    # loop_type == "count"
    count_number: int = 0  # 循环次数
    count_sleep_time: int = 0  # 休眠时间

    # loop_type == "for"
    for_variable_name: str = ""  # 循环变量名
    for_variable: str = ""  # 循环变量
    for_sleep_time: int = 0  # 休眠时间

    # loop_type == "while"
    while_comparator: str = ""  # 比对条件
    while_variable: str = ""  # 循环变量
    while_value: str = ""  # 循环值
    while_sleep_time: int = 0
    while_timeout: int = 0  # 超时时间


class TSqlController(TBaseController):
    """sql控制器"""
    value: str = ""
    step_type: typing.Literal["sql"]
    env_id: typing.Optional[int] = None
    source_id: typing.Optional[int] = None
    host: typing.Optional[str] = None
    user: typing.Optional[str] = None
    password: typing.Optional[str] = None
    port: typing.Optional[int] = None
    timeout: typing.Optional[int] = None  # 超时时间
    variable_name: typing.Optional[str] = None  # 变量赋值名称


# def init_step_id(teststeps: typing.List["TController"], parent_step_id=None):
#     """ 初始化步骤id --- 保证步骤唯一性，已经对应的层级
#         step_id: 步骤id
#         parent_id: 父级步骤的id
#     """
#     for step in teststeps:
#         if not step.step_id:
#             step.step_id = str(id_center.get_id())
#         if parent_step_id:
#             step.parent_step_id = parent_step_id
#
#         if hasattr(step, "teststeps"):
#             init_step_id(step.teststeps, step.step_id)
#
#         if hasattr(step, "setup_hooks"):
#             init_step_id(step.setup_hooks, step.step_id)
#
#         if hasattr(step, "teardown_hooks"):
#             init_step_id(step.teardown_hooks, step.step_id)


class TestCase(BaseModel):
    """测试用例"""
    config: TConfig
    step_type: typing.Literal["case"] = 'case'
    teststeps: typing.List[typing.Annotated[typing.Union[TApiController,
                                                         TScriptController,
                                                         TSqlController,
                                                         TWaitController,
                                                         TLoopController,
                                                         TIFController,
                                                         "TestCase"], Field(discriminator="step_type")]] = []


TController = typing.Union[TApiController,
                           TScriptController,
                           TSqlController,
                           TWaitController,
                           TLoopController,
                           TIFController,
                           TestCase]

TestCase.update_forward_refs()
TIFController.update_forward_refs()
TLoopController.update_forward_refs()


class TestCaseTime(BaseModel):
    start_at: float = 0
    duration: float = 0
    start_at_iso_format: str = ""


class TestCaseInOut(BaseModel):
    config_vars: VariablesMapping = {}
    export_vars: typing.Dict = {}


class RequestStat(BaseModel):
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    client_ip: str = "N/A"
    client_port: int = 0
    server_ip: str = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    method: typing.Optional[MethodEnum] = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = {}


class ResponseData(BaseModel):
    status_code: int
    headers: typing.Dict
    cookies: typing.Optional[Cookies]
    encoding: typing.Union[str, None] = None
    content_type: str
    body: typing.Union[str, bytes, typing.List, typing.Dict, None]


class ReqRespData(BaseModel):
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""

    success: bool = False
    req_resp: ReqRespData = {}
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: typing.Dict = {}
    extracts: typing.List = []


class StepResult(BaseModel):
    """测试步骤数据"""

    name: str = ""  # 步骤名称
    case_id: str = ""  # case_id
    index: int = 0  # case_id
    start_time: float = 0  # case_id
    duration: float = 0  # duration
    success: bool = False
    status: str = ""  # 步骤状态  success 成功  fail 失败  skip 跳过  err 错误
    step_type: str = ""
    step_tag: typing.Union[str, None] = None  # 标签
    message: str = ""  # err or message
    env_variables: VariablesMapping = {}
    variables: VariablesMapping = {}
    case_variables: VariablesMapping = {}
    step_result: typing.List['StepResult'] = None
    session_data: SessionData = None  # 请求信息
    pre_hook_data: typing.List['StepResult'] = []  # 前置
    post_hook_data: typing.List['StepResult'] = []  # 后置
    setup_hook_data: typing.List['StepResult'] = []  # 前置hook
    teardown_hook_data: typing.List['StepResult'] = []  # 后置hook
    export_vars: VariablesMapping = {}
    log: str = ""
    attachment: str = ""

    def dict(self, *args, **kwargs):
        """获取报告时去除 请求信息 避免报告数据太大"""
        kwargs["exclude"] = {"request", "response"}
        return super(StepResult, self).dict(*args, **kwargs)


StepResult.update_forward_refs()

#
# class StepResult(BaseModel):
#     """步骤结果, 对应请求数据或者步骤数据"""
#
#     name: str = ""  # teststep name
#     step_type: str = ""  # teststep type, request or testcase
#     success: bool = False
#     data: typing.Union[SessionData, typing.List["StepResult"]] = None
#     elapsed: float = 0.0  # teststep elapsed time
#     content_size: float = 0  # response content size
#     export_vars: VariablesMapping = {}
#     attachment: str = ""  # teststep attachment


StepResult.update_forward_refs()


#
# class IStep(object):
#     def name(self) -> str:
#         raise NotImplementedError
#
#     def type(self) -> str:
#         raise NotImplementedError
#
#     def struct(self) -> TStep:
#         raise NotImplementedError
#
#     def run(self, runner) -> StepResult:
#         # runner: HttpRunner
#         raise NotImplementedError


class TestCaseSummary(BaseModel):
    name: str
    success: bool
    case_id: typing.Optional[typing.Union[str, int]]
    start_time: typing.Union[float, str] = 0
    response_time: float = 0
    duration: float = 0
    run_count: int = 0
    actual_run_count: int = 0
    run_success_count: int = 0
    run_fail_count: int = 0
    run_skip_count: int = 0
    run_err_count: int = 0
    start_time_iso_format: str = ""
    in_out: TestCaseInOut = {}
    # message 记录错误信息
    message: str = ""
    log: str = ""
    step_results: typing.List[StepResult] = []


class PlatformInfo(BaseModel):
    zerorunner_version: str
    python_version: str
    platform: str


class TestSuite(BaseModel):
    config: TConfig
    testcases: typing.List[TestCase]


class Stat(BaseModel):
    total: int = 0
    success: int = 0
    fail: int = 0


class TestSuiteSummary(BaseModel):
    success: bool = False
    stat: Stat = Stat()
    time: TestCaseTime = TestCaseTime()
    platform: PlatformInfo
    testcases: typing.List[TestCaseSummary]
