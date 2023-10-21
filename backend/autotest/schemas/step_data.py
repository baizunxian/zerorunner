# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema
from zerorunner.model.step_model import TStep, ValidatorData, TSqlRequest, TIFRequest, TLoopRequest
from zerorunner.models import TRequest

from enum import Enum


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


class TStepData(TStep):
    """继承步骤类，方便入库存储"""
    step_type: str = Field(..., description="步骤类型")
    setup_hooks: typing.List[typing.Union["TStepData", str]] = []
    teardown_hooks: typing.List[typing.Union["TStepData", str]] = []
    variables: typing.List[typing.Any] = Field([], description="变量")
    validators: typing.List[ValidatorData] = Field([], alias="validators")
    request: TRequestData = Field(None, description="api请求参数")
    sql_request: TSqlData = Field(None, description="sql请求参数")
    children_steps: typing.List['TStepData'] = Field([], description="子步骤")
