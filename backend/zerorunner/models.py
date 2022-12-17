# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
from enum import Enum
from typing import Dict, Text, List, Union, Callable, Optional, Annotated, Any, Literal
from pydantic import BaseModel, Field, root_validator
from pydantic import HttpUrl

from zerorunner.snowflake import id_center

Name = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
ParametersMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
# Hooks = List[Union[Text, Dict[Text, Text]]]
Hooks = List[Any]
Export = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]


class MethodEnum(Text, Enum):
    """请求方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class TStepControllerEnum(Text, Enum):
    """步骤类型枚举"""
    case = "case"
    wait = "wait"
    script = "script"
    sql = "sql"
    extract = "extract"
    loop = "loop"
    IF = "IF"


TStepControllerDict = {
    "case": "用例",
    "wait": "等待控制器",
    "script": "脚本控制器",
    "sql": "sql控制器",
    "extract": "提取控制器",
    "loop": "循环控制器",
    "if": "条件控制器"
}


class LoopTypeEnum(Text, Enum):
    """循环类型枚举"""
    For = "for"
    Count = "count"
    While = "while"


class ComparatorEnum(Text, Enum):
    """比较方法枚举， 条件控制器， 循环控制 使用"""
    equals = "equals"
    not_equals = "not_equals"
    contains = "contains"
    not_contains = "not_contains"
    gt = "gt"
    lt = "lt"
    none = "none"
    not_none = "not_none"


class TStepDataStatusEnum(Text, Enum):
    """步骤数据状态"""
    success = "SUCCESS"
    fail = "FAILURE"
    skip = "SKIP"
    err = "ERROR"


class TStepLogType(Text, Enum):
    start = "开始"
    end = "结束"
    success = "成功"
    fail = "失败"
    skip = "跳过"
    err = "错误"
    wait = "等待"
    loop = "循环"
    condition = "条件"


class TStepTagEnum(Text, Enum):
    pre = "pre"  # 前置
    post = "post"  # 后置
    controller = "controller"  # 控制器


class TConfig(BaseModel):
    case_id: Union[Text, int] = ""
    name: Name
    verify: Verify = False
    base_url: BaseUrl = ""
    # 脚本函数
    functions: FunctionsMapping = {}  # TestCase 脚本函数
    # 环境变量
    env_variables: Union[VariablesMapping, Text] = {}
    # 请求头
    headers: VariablesMapping = {}
    # 配置变量
    variables: Union[VariablesMapping, Text] = {}
    # 参数
    parameters: Union[VariablesMapping, Text] = {}
    # setup_hooks: Hooks = []
    # teardown_hooks: Hooks = []
    export: Export = []
    # path: Text = None
    weight: int = 1


class TRequest(BaseModel):
    """requests.Request model"""

    method: MethodEnum
    url: Url
    params: Dict[Text, Text] = {}
    headers: Headers = {}
    req_json: Union[Dict, List, Text] = Field(None, alias="json")
    data: Union[Text, Dict[Text, Any]] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: Dict = {}  # used for upload files


class TBaseController(BaseModel):
    name: Name = ""
    value: Any = ""
    enable: bool = True  # 是否有效
    index: int = 0  # 顺序
    step_id: Text = None  # 唯一步骤id
    parent_step_id: Text = None  # 父级id  step_id


class ExtractData(BaseModel):
    name: Text = ""
    path: Text = ""
    extract_type: Text = ""  # 提取类型  jmespath


class TCaseController(TBaseController):
    case_id: Union[Text, int] = ''
    step_type: Literal['case']
    request: Union[TRequest, None] = None
    testcase: Union[Text, Callable, None] = None
    variables: VariablesMapping = {}
    # parameters 加入步骤 参数
    parameters: ParametersMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    message: Text = ''
    # used to extract request's response field
    extracts: List[ExtractData] = []
    # used to export session variables from referenced testcase
    export: Export = []
    validators: Validators = Field([], alias="validate")


class TScriptController(TBaseController):
    """脚本控制"""
    value: Optional[Text] = None
    step_type: Literal["script"]


class TWaitController(TBaseController):
    """等待控制器"""
    step_type: Literal["wait"]
    value: Optional[int] = None


class TIFController(TBaseController):
    step_type: Literal["if"]
    check: Text = ""  # 校验变量
    comparator: Text = ""  # 对比规则
    expect: Text = ""  # 对比值
    remarks: Text = ""  # 备注
    teststeps: List["TController"] = []


class TLoopController(TBaseController):
    """循环控制器"""
    step_type: Literal["loop"]
    teststeps: List["TController"] = []
    loop_type: Literal["count", "for", "while"]
    # loop_type == "count"
    count_number: int = 0  # 循环次数
    count_sleep_time: int = 0  # 休眠时间

    # loop_type == "for"
    for_variable_name: Text = ""  # 循环变量名
    for_variable: Text = ""  # 循环变量
    for_sleep_time: int = 0  # 休眠时间

    # loop_type == "while"
    while_comparator: Text = ""  # 比对条件
    while_variable: Text = ""  # 循环变量
    while_value: Text = ""  # 循环值
    while_sleep_time: int = 0
    while_timeout: int = 0  # 超时时间


class TSqlController(TBaseController):
    """sql控制器"""
    value: Text = ""
    step_type: Literal["sql"]
    env_id: Optional[int] = None
    source_id: Optional[int] = None
    host: Optional[Text] = None
    user: Optional[Text] = None
    password: Optional[Text] = None
    port: Optional[int] = None
    timeout: Optional[int] = None  # 超时时间
    variable_name: Optional[Text] = None  # 变量赋值名称


TController = Union[TCaseController,
                    TScriptController,
                    TSqlController,
                    TWaitController,
                    TLoopController,
                    TIFController]

TIFController.update_forward_refs()
TLoopController.update_forward_refs()


def init_step_id(teststeps: List[TController], parent_step_id=None):
    """ 初始化步骤id --- 保证步骤唯一性，已经对应的层级
        step_id: 步骤id
        parent_id: 父级步骤的id
    """
    for step in teststeps:
        if not step.step_id:
            step.step_id = str(id_center.get_id())
        if parent_step_id:
            step.parent_step_id = parent_step_id

        if hasattr(step, "teststeps"):
            init_step_id(step.teststeps, step.step_id)

        if hasattr(step, "setup_hooks"):
            init_step_id(step.setup_hooks, step.step_id)

        if hasattr(step, "teardown_hooks"):
            init_step_id(step.teardown_hooks, step.step_id)


class TestCase(BaseModel):
    """测试用例"""
    config: TConfig
    teststeps: List[Annotated[TController, Field(discriminator="step_type")]] = []

    @root_validator(pre=True)
    def root_validator_step(cls, obj):
        init_step_id(obj.get('teststeps', []))
        return obj


class TestCaseTime(BaseModel):
    start_at: float = 0
    duration: float = 0
    start_at_iso_format: Text = ""


class TestCaseInOut(BaseModel):
    config_vars: VariablesMapping = {}
    export_vars: Dict = {}


class RequestStat(BaseModel):
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    client_ip: Text = "N/A"
    client_port: int = 0
    server_ip: Text = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    method: MethodEnum = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: Union[Text, bytes, List, Dict, None] = {}


class ResponseData(BaseModel):
    status_code: int
    headers: Dict
    cookies: Cookies
    encoding: Union[Text, None] = None
    content_type: Text
    body: Union[Text, bytes, List, Dict, None]


class ReqRespData(BaseModel):
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""

    success: bool = False
    req_resp: ReqRespData = {}
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: Dict = {}


class StepData(BaseModel):
    """测试步骤数据"""

    name: Text = ""  # 步骤名称
    case_id: Text = ""  # case_id
    index: int = 0  # case_id
    start_time: float = 0  # case_id
    duration: float = 0  # duration
    success: bool = False
    status: Text = ""  # 步骤状态  success 成功  fail 失败  skip 跳过  err 错误
    step_id: Text = None  # 步骤id
    parent_step_id: Text = None  # 父级步骤id
    step_type: Text = ""
    step_tag: Union[Text, None] = None  # pre 前置，post 后置，controller 控制器
    message: Text = ""  # err or message
    env_variables: VariablesMapping = {}
    variables: VariablesMapping = {}
    step_data: List['StepData'] = None
    session_data: SessionData = None  # 请求信息
    pre_hook_data: List['StepData'] = []  # 前置
    post_hook_data: List['StepData'] = []  # 后置
    export_vars: VariablesMapping = {}

    def dict(self, *args, **kwargs):
        """获取报告时去除 请求信息 避免报告数据太大"""
        if "request" in self.variables:
            self.variables.pop("request", None)
        if "response" in self.variables:
            self.variables.pop("response", None)
        return super(StepData, self).dict(*args, **kwargs)


StepData.update_forward_refs()


class TestCaseSummary(BaseModel):
    name: Text
    success: bool
    case_id: Text
    start_time: float = 0
    duration: float = 0
    run_count: int = 0
    actual_run_count: int = 0
    run_success_count: int = 0
    run_fail_count: int = 0
    run_skip_count: int = 0
    run_err_count: int = 0
    start_time_iso_format: Text = ""
    in_out: TestCaseInOut = {}
    # message 记录错误信息
    message: Text = ""
    log: Text = ""
    step_datas: List[StepData] = []


class PlatformInfo(BaseModel):
    zerorunner_version: Text
    python_version: Text
    platform: Text


class TestSuite(BaseModel):
    config: TConfig
    testcases: List[TestCase]


class Stat(BaseModel):
    total: int = 0
    success: int = 0
    fail: int = 0


class TestSuiteSummary(BaseModel):
    success: bool = False
    stat: Stat = Stat()
    time: TestCaseTime = TestCaseTime()
    platform: PlatformInfo
    testcases: List[TestCaseSummary]
