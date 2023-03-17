import json
import typing

from pydantic import root_validator, BaseModel, Field

from autotest.exceptions import ParameterError
from autotest.schemas.base import BaseSchema
from zerorunner.models import TController, ExtractData, MethodEnum


class ApiQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List = Field(None, description="ids")
    name: str = Field(None, description="接口名")
    api_status: int = Field(None, description="接口状态")
    api_type: int = Field(None, description="api 类型")
    code: str = Field(None, description="接口code")
    sort_type: str = Field(None, description="排序类型")
    priority: int = Field(None, description="优先级")
    project_id: int = Field(None, description="项目id")
    project_ids: typing.List[int] = Field(None, description="项目ids")
    module_id: int = Field(None, description="模块id")
    module_ids: typing.List[int] = Field(None, description="ids")
    project_name: str = Field(None, description="项目名")
    order_field: str = Field(None, description="排序字段")
    created_by: int = Field(None, description="创建人id")
    created_by_name: str = Field(None, description="创建人")


class ApiId(BaseModel):
    id: int = Field(..., description="id")


class ApiRunBodySchema(BaseModel):
    """"""
    name: str = Field(None, description="id")
    # user_id: int = Field(None, description="id")
    case_status: int = Field(None, description="id")
    case_type: int = Field(None, description="id")
    code: str = Field(None, description="id")
    run_type: int = Field(None, description="id")
    include: str = Field(None, description="id")
    testcase: str = Field(None, description="id")
    code_id: int = Field(None, description="id")
    priority: int = Field(None, description="id")
    config_id: int = Field(None, description="id")
    project_id: int = Field(None, description="id")
    module_id: int = Field(None, description="id")
    created_by: int = Field(None, description="id")

    @root_validator
    def root_validator(cls, data):
        if data['testcase']:
            data['testcase'] = json.loads(data['testcase'])
        if 'include' in data:
            data["include"] = list(map(int, data["include"].split(","))) if data["include"] else []
        return data


class ApiRunSchema(BaseModel):
    """运行用例"""

    id: int = Field(None, description="id")
    ids: typing.List[int] = Field(None, description="ids")
    env_id: str = Field(None, description="环境id")
    name: str = Field(None, description="名称")
    run_type: int = Field(None, description="运行类型")
    run_mode: str = Field(None, description="运行模式")
    number_of_run: int = Field(None, description="运行次数")

    @root_validator
    def root_validator(cls, data):
        if not data.get("base_url"):
            data['base_url'] = ""
        if not data.get("id"):
            raise ParameterError("请选择用例!")
        return data


class ApiRunBatchSchema(BaseModel):
    """批量运行用例"""

    ids: typing.List[typing.Union[str, int]] = Field([], description="")
    base_url: str = Field(None, description="id")
    name: str = Field(None, description="id")
    project_id: int = Field(None, description="id")
    run_type: str = Field(None, description="id")
    run_mode: int = Field(None, description="id")
    ex_user_id: int = Field(None, description="id")
    testcase_dir_path: str = Field(None, description="id")

    @root_validator(pre=True)
    def root_validator(cls, data):
        if not data.get("base_url", None):
            data['base_url'] = ""
        if 'ids' in data:
            data['ids'] = list(map(int, data.get('ids')))
        return data


class ApiBaseSchema(BaseModel):
    key: str = Field(None, description="")
    value: str = Field(None, description="")
    remarks: str = Field(None, description="")


class ApiValidatorsSchema(BaseModel):
    mode: str = Field("", description="")
    check: str = Field("", description="")
    expect: str = Field("", description="")
    comparator: str = Field("", description="")


class ApiBodySchema(BaseModel):
    mode: str = Field("", description="")
    data: str = Field("", description="")
    language: str = Field("", description="")


class ApiHooksSchema(BaseModel):
    name: str = Field(None, description="")
    index: typing.Union[str, int] = ""
    value: typing.Union[typing.Any] = ""
    enable: bool = ""
    step_type: str = Field(None, description="")


class StepScriptSchema(ApiHooksSchema):
    pass


class StepSqlSchema(ApiHooksSchema):
    env_id: int = Field(None, description="")
    source_id: int = Field(None, description="")
    variable_name: str = Field("", description="")
    timeout: int = Field(None, description="")


class StepWaitSchema(ApiHooksSchema):
    pass


class ApiInfoIn(BaseModel):
    """用例保存更新"""
    id: int = Field(None, description="")
    name: str = Field(..., description="")
    project_id: int = Field(..., description="")
    module_id: int = Field(..., description="")
    case_status: int = Field(None, description="")
    code_id: int = Field(None, description="")
    code: str = Field(None, description="")
    priority: int = Field(None, description="")
    case_tag: str = Field(None, description="")
    method: str = Field(None, description="")
    url: str = Field(None, description="")
    request_body: ApiBodySchema = Field({}, description="")
    pre_steps: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    post_steps: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    setup_hooks: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    teardown_hooks: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    variables: typing.List[ApiBaseSchema] = Field([], description="")
    headers: typing.List[ApiBaseSchema] = Field([], description="")
    validators: typing.List[ApiValidatorsSchema] = Field([], description="")
    extracts: typing.List[ExtractData] = Field([], description="")
    tags: typing.List[str] = Field([], description="")
    remarks: str = Field(None, description="")


class ApiInfoRun(BaseModel):
    id: int = Field(0, description="")
    index: int = Field(0, description="")
    name: str = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    case_status: int = Field(None, description="")
    code_id: int = Field(None, description="")
    code: str = Field(None, description="")
    priority: int = Field(None, description="")
    case_tag: str = Field(None, description="id")
    enable: bool = Field(True, description="")
    method: MethodEnum = Field(None, description="")
    url: str = Field(None, description="")
    env_id: int = Field(None, description="")
    request_body: ApiBodySchema = Field({}, description="")
    setup_hooks: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    teardown_hooks: typing.List[typing.Annotated[TController, Field(discriminator="step_type")]] = Field([], description="")
    variables: typing.List[ApiBaseSchema] = Field([], description="")
    headers: typing.List[ApiBaseSchema] = Field([], description="")
    validators: typing.List[ApiValidatorsSchema] = Field([], description="")
    extracts: typing.List[ExtractData] = Field([], description="")
