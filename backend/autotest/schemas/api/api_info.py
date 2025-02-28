import json
import typing

from pydantic import root_validator, BaseModel, Field

from autotest.schemas.base import BaseSchema
from autotest.schemas.step_data import TStepData, TRequestData, ApiBaseSchema
from zerorunner.models.base import MethodEnum
from zerorunner.models.step_model import ExtractData


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
    id: int = Field(None, description="id")


class ApiIds(BaseModel):
    ids: typing.List[typing.Union[str, int]] = Field(None, description="id")


class ApiDetailId(BaseModel):
    id: int = Field(None, description="id")
    ids: typing.List[typing.Union[str, int]] = Field(None, description="id")


class ApiRunSchema(BaseModel):
    """运行用例"""

    id: int = Field(None, description="id")
    ids: typing.List[int] = Field(None, description="ids")
    env_id: str = Field(None, description="环境id")
    name: str = Field(None, description="名称")
    run_type: str = Field("api", description="运行模式")
    run_mode: int = Field(None, description="运行类型 10 同步， 20 异步, 30定时任务")
    number_of_run: int = Field(None, description="运行次数")
    exec_user_id: int = Field(None, description="执行人id")
    exec_user_name: str = Field(None, description="执行人")
    api_run_mode: str = Field(None, description="api运行模式  one 单个， batch 批量")


class ApiBatchRunSchema(BaseModel):
    """批量运行api"""

    ids: typing.List[int] = Field(None, description="ids")
    env_id: str = Field(None, description="环境id")
    name: str = Field(None, description="名称")


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


class ApiValidatorsSchema(BaseModel):
    mode: str = Field("", description="")
    check: str = Field("", description="")
    expect: str = Field("", description="")
    comparator: str = Field("", description="")


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


class ApiInfoIn(TStepData):
    """用例保存更新"""
    id: int = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    status: int = Field(None, description="")
    env_id: int = Field(None, description="")
    code_id: int = Field(None, description="")
    code: str = Field(None, description="")
    priority: int = Field(None, description="")
    method: str = Field(None, description="")
    url: str = Field(None, description="")
    tags: typing.List[str] = Field([], description="")
    remarks: str = Field(None, description="")
    # validators: typing.List[typing.Any] = []
    # pre_steps: typing.List[typing.Annotated[TStepData, Field(discriminator="step_type")]] = Field([], description="")
    # post_steps: typing.List[typing.Annotated[TStepData, Field(discriminator="step_type")]] = Field([], description="")
    headers: typing.List[ApiBaseSchema] = Field([], description="")
    children_steps: typing.List['ApiInfoIn'] = Field([], description="子步骤")


class ApiRun(BaseModel):
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: int = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    code_id: int = Field(None, description="")
    code: str = Field(None, description="")
    priority: int = Field(None, description="")
    status: int = Field(None, description="")
    tags: typing.List[str] = Field([], description="")
    step_data: typing.Union[TStepData, typing.List[TStepData]] = Field(None, description="步骤")
    step_rely: int = Field(None, description="步骤依赖 1依赖，0 不依赖")


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
    step_type: int = Field(..., description="")
    request: TRequestData = Field({}, description="")
    setup_hooks: typing.Union[TStepData, typing.List[TStepData]] = Field(None, description="步骤")
    teardown_hooks: typing.Union[TStepData, typing.List[TStepData]] = Field(None, description="步骤")
    variables: typing.List[ApiBaseSchema] = Field([], description="")
    headers: typing.List[ApiBaseSchema] = Field([], description="")
    validators: typing.List[ApiValidatorsSchema] = Field([], description="")
    extracts: typing.List[ExtractData] = Field([], description="")
