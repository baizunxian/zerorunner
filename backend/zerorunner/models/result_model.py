# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field

from zerorunner.models.base import VariablesMapping, MethodEnum, Url, Headers, Cookies
from zerorunner.models.step_model import TSqlRequest


class RequestStat(BaseModel):
    """请求统计"""
    content_size: float = Field(0, description="响应内容大小")
    response_time_ms: float = Field(0, description="响应时间 毫秒")
    elapsed_ms: float = Field(0, description="过程时间")


class AddressData(BaseModel):
    """地址信息"""
    client_ip: str = Field("N/A", description="客户端ip")
    client_port: int = Field(0, description="客户端端口")
    server_ip: str = Field("N/A", description="服务端ip")
    server_port: int = Field(0, description="服务端端口")


class RequestData(BaseModel):
    """请求数据"""
    method: typing.Optional[MethodEnum] = Field(MethodEnum.GET, description="请求方法")
    url: Url = Field(..., description="url")
    headers: Headers = Field({}, description="请求头")
    cookies: Cookies = Field({}, description="cookies")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field({}, description="body")


class ResponseData(BaseModel):
    """响应数据"""
    status_code: int = Field(..., description="状态码")
    headers: typing.Dict = Field(..., description="响应头")
    cookies: typing.Optional[Cookies] = Field(None, description="cookies")
    encoding: typing.Union[str, None] = Field(None, description="encoding")
    content_type: str = Field(..., description="类型")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field(None, description="body")


class ReqRespData(BaseModel):
    """请求响应数据"""
    request: RequestData = Field(..., description="请求数据")
    response: ResponseData = Field(..., description="响应数据")


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""
    success: bool = Field(False, description="是否成功")
    req_resp: ReqRespData = Field({}, description="请求，响应数据")
    stat: RequestStat = Field(RequestStat(), description="时间")
    address: AddressData = Field(AddressData(), description="地址")
    validators: typing.Dict = Field({}, description="校验")
    extracts: typing.List = Field([], description="提取")


class SqlSessionData(TSqlRequest):
    """sql会话数据"""

    success: bool = Field(False, description="是否成功")
    execution_result: typing.Any = Field(None, description="执行结果")


class UiSessionData(BaseModel):
    """ui会话数据"""
    action: str = Field(None, description="动作")
    data: str = Field(None, description="输入数据")
    location_method: str = Field(None, description="定位方法")
    location_value: str = Field(None, description="定位值")
    cookie: typing.Dict = Field(None, description="cookie")
    locator_data: typing.Dict = Field({}, description="定位器数据")
    validators: typing.Dict = Field({}, description="校验")
    screenshot_file_base64: str = Field(None, description="截图base64")


class StepResult(BaseModel):
    """测试步骤数据"""

    index: int = Field(0, description="index")
    name: str = Field("", description="步骤名称")
    step_id: typing.Union[str, int] = Field(None, description="步骤id")
    parent_step_id: typing.Union[str, int] = Field(None, description="父步骤id")
    case_id: typing.Union[str, int] = Field(None, description="case_id")
    source_id: typing.Union[int, str] = Field(None, description="来源id")
    start_time: float = Field(0, description="开始时间")
    duration: float = Field(0, description="执行耗时")
    success: bool = Field(False, description="是否成功")
    status: str = Field("", description="步骤状态  success 成功  fail 失败  skip 跳过  err 错误")
    step_type: str = Field("", description="步骤类型")
    step_tag: typing.Union[str, None] = Field(None, description="步骤标签")
    env_variables: VariablesMapping = Field({}, description="环境变量")
    variables: VariablesMapping = Field({}, description="变量")
    case_variables: VariablesMapping = Field({}, description="用例变量")
    step_result: typing.List['StepResult'] = Field([], description="步骤结果")
    session_data: typing.Union[SessionData, SqlSessionData, UiSessionData] = Field(None, description="请求信息")
    setup_hook_results: typing.List['StepResult'] = Field([], description="前置hook")
    teardown_hook_results: typing.List['StepResult'] = Field([], description="后置hook")
    export_vars: VariablesMapping = Field({}, description="")
    message: str = Field("", description="错误信息等")
    log: str = Field("", description="执行log")

    # attachment: str = Field("", description="附件")

    def dict(self, *args, **kwargs):
        """获取报告时去除 请求信息 避免报告数据太大"""
        kwargs["exclude"] = {"request", "response"}
        return super(StepResult, self).dict(*args, **kwargs)


class TestCaseInOut(BaseModel):
    """用例输入输出"""
    config_vars: VariablesMapping = Field({}, description="配置参数")
    export_vars: typing.Dict = Field({}, description="导出参数")


class TestCaseSummary(BaseModel):
    """用例汇总数据"""
    name: str = Field(..., description="报告名称")
    success: bool = Field(..., description="是否成功")
    case_id: typing.Union[str, int] = Field(None, description="用例id")
    source_id: typing.Union[str, int] = Field(None, description="来源id")
    start_time: typing.Union[float, str] = Field(0, description="开始时间")
    response_time: float = Field(0, description="请求时间")
    duration: float = Field(0, description="耗时")
    run_count: int = Field(0, description="运行数量")
    actual_run_count: int = Field(0, description="实际执行数量")
    run_success_count: int = Field(0, description="运行成功数")
    run_fail_count: int = Field(0, description="运行错误数")
    run_skip_count: int = Field(0, description="运行跳过数")
    run_err_count: int = Field(0, description="运行错误数")
    start_time_iso_format: str = Field("", description="运行时间系统时间")
    in_out: TestCaseInOut = Field({}, description="输出")
    # message 记录错误信息
    message: str = Field("", description="信息")
    log: str = Field("", description="日志")
    step_results: typing.List[StepResult] = Field([], description="步骤结果")


class PlatformInfo(BaseModel):
    """平台信息"""
    zerorunner_version: str = Field(..., description="版本号")
    python_version: str = Field(..., description="python版本")
    platform: str = Field(..., description="机器信息")


class Stat(BaseModel):
    """统计数据"""
    total: int = Field(0, description="总数")
    success: int = Field(0, description="成功数量")
    fail: int = Field(0, description="失败数量")


class TestCaseTime(BaseModel):
    """用例时间"""
    start_at: float = Field(0, description="时间")
    duration: float = Field(0, description="过程耗时")
    start_at_iso_format: str = Field("", description="开始系统时间")


class TestSuiteSummary(BaseModel):
    """测试套件汇总数据"""
    success: bool = Field(False, description="是否成功")
    stat: Stat = Field(Stat(), description="统计")
    time: TestCaseTime = Field(TestCaseTime(), description="时间")
    platform: PlatformInfo = Field(..., description="系统信息")
    testcases: typing.List[TestCaseSummary] = Field(..., description="用例列表")
