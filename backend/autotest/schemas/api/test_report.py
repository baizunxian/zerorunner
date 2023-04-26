import typing

from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema


class TestReportQuery(BaseSchema):
    """测试报告查询"""

    id: int = Field(None, description="")
    ids: typing.List[int] = Field(None, description="")
    project_name: str = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    execute_user_name: str = Field(None, description="")
    min_and_max: str = Field(None, description="")
    report_type: str = Field(None, description="")
    name: str = Field(None, description="")
    run_user_name: str = Field(None, description="")
    user_ids: typing.List[int] = Field(None, description="")
    created_by: int = Field(None, description="")
    project_ids: typing.List[int] = Field(None, description="")


class TestReportSaveSchema(BaseModel):
    """测试报告保持"""

    id: int = Field(None, description="")
    name: str = Field(None, description="")
    start_time: str = Field(None, description="")
    duration: float = Field(None, description="")
    case_id: typing.Union[str, int] = Field(None, description="")
    run_mode: str = Field(None, description="运行模式")
    run_type: int = Field(None, description="运行类型 10 同步， 20 异步")
    success: bool = Field(False, description="")
    run_count: int = Field(0, description="")
    actual_run_count: int = Field(0, description="")
    run_success_count: int = Field(0, description="")
    run_fail_count: int = Field(0, description="")
    run_skip_count: int = Field(0, description="")
    run_err_count: int = Field(0, description="")
    run_log: str = Field("", description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    env_id: int = Field(None, description="")

    # @root_validator
    # def root_validator(cls, data):
    #     start_time = data.get("start_time", None)
    #     if start_time in data:
    #         data['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)) \
    #             if start_time and isinstance(start_time, (float, int)) else None
    #     return data


class TestReportMakeSchema(BaseModel):
    """测试报告处理"""

    details: typing.List[typing.Dict] = Field(None, description="")
    platform: typing.Dict = Field(None, description="")
    stat: typing.Dict = Field(None, description="")
    time: typing.Dict = Field(None, description="")
    success: bool = Field(None, description="")


class TestReportId(BaseModel):
    """测试报告处理"""

    id: int = Field(..., description="")


class TestReportDetailQuery(TestReportId):
    """测试报告处理"""
    name: str = Field(None, description="名称")
    url: str = Field(None, description="url地址")
    api_name: str = Field(None, description="接口名称")
    step_type: str = Field(None, description="步骤类型")
    status_list: typing.List[str] = Field(None, description="状态")
    parent_step_id: int = Field(None, description="")
