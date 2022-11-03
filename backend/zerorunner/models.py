# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
from enum import Enum
from typing import Any
from typing import Dict, Text, Union, Callable
from typing import List

from pydantic import BaseModel, Field, validator
from pydantic import HttpUrl

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
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


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
    # 变量
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


class TStep(BaseModel):
    name: Name
    case_id: Union[Text, int] = ''
    request: Union[TRequest, None] = None
    testcase: Union[Text, Callable, None] = None
    variables: VariablesMapping = {}
    # parameters 加入步骤 参数
    parameters: ParametersMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    message: Text = ''
    # used to extract request's response field
    extract: VariablesMapping = {}
    # used to export session variables from referenced testcase
    export: Export = []
    validators: Validators = Field([], alias="validate")
    # validate_script: List[Text] = []
    # # 脚本
    # script_codes: List[Text] = []


# 用例控制器
class BaseTController(BaseModel):
    """步骤控制器"""
    name: Text = ""
    value: Any = ""
    step_type: Text = ""
    enable: bool = False  # 是否有效


class SqlController(BaseTController):
    source_id: int = None,
    host: Text = ""
    user: Text = ""
    password: Text = ""
    port: int = 3306
    timeout: int = None  # 超时时间
    variable_name: Text = ""  # 变量赋值名称


class WaitController(BaseTController):
    """等待控制器"""
    value: int = 0
    pass


class ScriptController(BaseTController):
    """脚本控制器"""
    pass


class CaseController(BaseTController, TStep):
    """用例控制器"""
    pass


class JsonPathData(BaseModel):
    name: Text = ""  # 提取变量名
    path: Text = ""  # 提取JsonPath路径


class ExtractController(BaseTController):
    value: List[JsonPathData]


Controllers = (SqlController, WaitController, ScriptController, JsonPathData, TStep,)


class TestCase(BaseModel):
    config: TConfig
    teststeps: List[Any]

    @validator('teststeps')
    def teststeps_match(cls, teststeps, values, **kwargs):
        steps = []
        for teststep in teststeps:
            if not isinstance(teststep, Controllers):
                raise ValueError("类型错误！")
            steps.append(teststep)
        return steps


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
    # in most cases, req_resps only contains one request & response
    # while when 30X redirect occurs, req_resps will contain multiple request & response
    req_resps: List[ReqRespData] = []
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: Dict = {}


class StepData(BaseModel):
    """测试步骤数据"""

    name: Text = ""  # teststep name
    case_id: Text = ""  # case_id
    success: bool = False
    status: Text = ""  # 步骤状态
    message: Text = ""  # err or message
    variables: VariablesMapping = {}
    data: Union[SessionData, List['StepData']] = None
    export_vars: VariablesMapping = {}

    def dict(self, *args, **kwargs):
        if "request" in self.variables:
            self.variables.pop("request", None)
        if "response" in self.variables:
            self.variables.pop("response", None)
        return super(StepData, self).dict()


StepData.update_forward_refs()


class TestCaseSummary(BaseModel):
    name: Text
    success: bool
    case_id: Text
    time: TestCaseTime
    in_out: TestCaseInOut = {}
    # message 记录错误信息
    message: Text = ""
    log: Text = ""
    step_datas: List[StepData] = []


class PlatformInfo(BaseModel):
    zerorunner_version: Text
    python_version: Text
    platform: Text


class TestCaseRef(BaseModel):
    name: Text
    base_url: Text = ""
    testcase: Text
    variables: VariablesMapping = {}


class TestSuite(BaseModel):
    config: TConfig
    testcases: List[TestCaseRef]


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
