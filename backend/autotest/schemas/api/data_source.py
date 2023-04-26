import typing

from pydantic import root_validator, BaseModel, Field

from autotest.exceptions.exceptions import ParameterError
from autotest.schemas.base import BaseSchema


class SourceQuery(BaseSchema):
    id: int = Field(None, description="id")
    source_type: str = Field("mysql", description="数据源类型")
    name: str = Field(None, description="")
    source_ids: typing.List[int] = Field(None, description="")


class SourceIn(BaseModel):
    id: int = Field(None, description="id")
    type: str = Field(None, description="")
    name: str = Field(..., description="")
    host: str = Field(None, description="")
    port: str = Field(None, description="")
    user: str = Field(None, description="")
    password: str = Field(None, description="")


class EnvListSchema(BaseModel):
    """环境序列化"""
    name: typing.Text
    url: str = Field(None, description="url")
    remarks: str = Field(None, description="备注")


class SourceId(BaseModel):
    """环境序列化"""
    id: int = Field(..., description="id")


class EnvIn(BaseModel):
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    domain_name: str = Field(None, description="")
    remarks: str = Field(None, description="")
    headers: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="")
    variables: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="")
    data_sources: typing.List[int] = Field(None, description="")
