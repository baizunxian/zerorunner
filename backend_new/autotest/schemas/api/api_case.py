import typing
from pydantic import root_validator, BaseModel, Field

from autotest.schemas.api.api_info import ApiBaseSchema
from autotest.schemas.base import BaseSchema
from autotest.schemas.step_data import TStepData
from zerorunner.model.step_model import TIFRequest, TLoopRequest


class ApiCaseQuery(BaseSchema):
    """用例查询"""
    id: int = Field(None, description="")
    ids: typing.List[int] = Field(None, description="")
    name: str = Field(None, description="")
    module_name: str = Field(None, description="")
    project_name: str = Field(None, description="")
    project_id: int = Field(None, description="项目id")
    project_ids: typing.List[int] = Field(None, description="项目ids")
    order_field: str = Field(None, description="")
    created_by: int = Field(None, description="")
    created_by_name: str = Field(None, description="")
    suite_type: int = Field(None, description="")
    user_ids: typing.List[int] = Field(None, description="user ids")


class ApiCaseIdsQuery(BaseSchema):
    """用例查询"""
    ids: typing.List[int] = Field(None, description="")


class ApiCaseListSchema(BaseSchema):
    """用例列表"""
    name: str = Field(None, description="")
    project_name: str = Field(None, description="")
    project_id: int = Field(None, description="")
    include: str = Field(None, description="")
    remarks: str = Field(None, description="")
    config_id: int = Field(None, description="")
    run_status: str = Field(None, description="")

    @root_validator
    def root_validator(cls, data):
        if 'include' in data:
            data['include'] = list(map(int, data['include'].split(','))) if data['include'] else []
        return data


class TCaseRequestData(BaseModel):
    api_id: typing.Union[str, int] = Field(..., description="api id")
    name: str = Field(None, description="用例名称")


class TCaseStepData(TStepData):
    """测试用例数据"""
    sub_steps: typing.List['TCaseStepData'] = Field([], description="子步骤， 当前字段只对 if  loop 类型有效")
    request: TCaseRequestData = Field(None, description="引用用例")


TCaseStepData.update_forward_refs()


class ApiCaseIn(BaseModel):
    """用例保存"""
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: str = Field(None, description="")
    project_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    step_rely: int = Field(1, description="")
    step_data: typing.List[TCaseStepData] = Field(None, description="步骤类容")
    headers: typing.List[ApiBaseSchema] = Field(None, description="请求头参数")
    variables: typing.List[ApiBaseSchema] = Field(None, description="变量参数")


class TestCaseRun(BaseModel):
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: int = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    step_data: typing.List[TCaseStepData] = Field([], description="步骤数据")
    step_rely: int = Field(None, description="步骤依赖 1依赖，0 不依赖")
    headers: typing.List[ApiBaseSchema] = Field(None, description="请求头参数")
    variables: typing.List[ApiBaseSchema] = Field(None, description="变量参数")


class ApiCaseId(BaseSchema):
    id: int = Field(..., description="")


class ApiTestCaseRun(BaseSchema):
    id: int = Field(..., description="用例id")
    env_id: int = Field(None, description="环境id")
