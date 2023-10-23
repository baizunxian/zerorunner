# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from enum import Enum

from pydantic import BaseModel, Field, root_validator

from autotest.schemas.base import BaseSchema
from zerorunner.models.base import TStepTypeEnum
from zerorunner.models.step_model import TStep, ValidatorData, TSqlRequest, TRequest, TIFRequest, TWaitRequest, \
    TScriptRequest, TLoopRequest, TUiRequest


class RequestMode(str, Enum):
    """请求模式"""
    RAW = "raw"
    FORM_DATA = "form_data"
    FILE = "file"
    X_WWW_FORM_URLENCODED = "x_www_form_urlencoded"
    none = "none"


class RawLanguageEnum(str, Enum):
    """raw语言"""
    JSON = "json"
    TEXT = "text"
    HTML = "html"
    XML = "xml"
    JAVASCRIPT = "javascript"
    CSS = "css"
    none = "none"


class ApiBodyFileValueSchema(BaseSchema):
    id: str = Field("", description="文件id")
    name: str = Field("", description="文件名称")


class ApiBodyFileDataSchema(BaseSchema):
    key: str = Field("", description="form表单名称")
    value: typing.Union[str, ApiBodyFileValueSchema] = Field("", description="文件数据")
    type: str = Field("", description="类型 file text")


class ApiBaseSchema(BaseModel):
    key: str = Field(None, description="")
    value: typing.Any = Field(None, description="")
    remarks: str = Field(None, description="")


class TRequestData(TRequest):
    mode: typing.Union[RequestMode, str] = Field("", description="模式 raw  form-data 等")
    data: typing.Union[str, typing.List[typing.Union[ApiBodyFileDataSchema, ApiBaseSchema]]] = Field(None,
                                                                                                     description="数据json 数据 或者form-data数据等")
    language: typing.Union[RawLanguageEnum, str] = Field("", description="raw 中包含json text 等")
    upload: typing.Dict = Field({}, description="上传文件的数据")
    headers: typing.List[typing.Any] = Field([], description="请求头")


class TSqlData(TSqlRequest):
    env_id: typing.Optional[int] = None
    source_id: typing.Optional[int] = None


class TStepSqlData(BaseModel):
    """sql控制器"""
    # sql
    value: str = ""
    step_type: typing.Literal["sql"] = Field("sql", description="数据类型")
    env_id: int = Field(None, description="环境id")
    source_id: int = Field(None, description="数据源id")
    host: int = Field(None, description="host")
    user: int = Field(None, description="user")
    password: str = Field(None, description="password")
    port: int = Field(None, description="port")
    timeout: int = Field(None, description="超时时间")
    variable_name: str = Field(None, description="赋值的变量名称")


TStepRequest = typing.Annotated[
    typing.Union[TRequestData, TSqlData, TIFRequest, TWaitRequest, TScriptRequest, TLoopRequest, TUiRequest], Field(
        discriminator='step_type')]


class TStepData(TStep):
    """继承步骤类，方便入库存储"""
    step_type: str = Field(..., description="步骤类型")
    setup_hooks: typing.List["TStepData"] = []
    teardown_hooks: typing.List["TStepData"] = []
    variables: typing.List[typing.Any] = Field([], description="变量")
    validators: typing.List[ValidatorData] = Field([], alias="validators")
    request: typing.Union[TStepRequest] =None
    children_steps: typing.List["TStepData"] = Field([], description="子步骤")

    # @root_validator(pre=True)
    # def customize_serialization(cls, values):
    #     if not values:
    #         return values
    #     request = values.get("request", None)
    #     setup_hooks = values.get("setup_hooks", [])
    #     teardown_hooks = values.get("setup_hooks", [])
    #     children_steps = values.get("children_steps", [])
    #     if request:
    #         values = get_request_model(values)
    #     values['setup_hooks'] = [get_request_model(hook) for hook in setup_hooks if setup_hooks]
    #     values['teardown_hooks'] = [get_request_model(hook) for hook in setup_hooks if teardown_hooks]
    #     values['children_steps'] = [get_request_model(children) for children in children_steps if children_steps]
    #     return values


def get_request_model(values: typing.Any) -> typing.Any:
    request = values.get("request", None)
    typing.Annotated
    step_type = values.get('step_type')
    if step_type == TStepTypeEnum.api.value:
        new_request = TRequestData.parse_obj(request)
    elif step_type == TStepTypeEnum.loop.value:
        new_request = TLoopRequest.parse_obj(request)
    elif step_type == TStepTypeEnum.sql.value:
        new_request = TSqlData.parse_obj(request)
    elif step_type == TStepTypeEnum.IF.value.lower():
        new_request = TIFRequest.parse_obj(request)
    elif step_type == TStepTypeEnum.wait.value:
        new_request = TWaitRequest.parse_obj(request)
    elif step_type == TStepTypeEnum.script.value:
        new_request = TScriptRequest.parse_obj(request)
    elif step_type == TStepTypeEnum.ui.value:
        new_request = TUiRequest.parse_obj(request)
    else:
        raise ValueError(f"不支持的类型{step_type}")
    values["request"] = new_request
    return values
