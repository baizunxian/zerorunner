import typing

from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema


class EnvQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List[typing.Union[int, str]] = Field(None, description="ids")
    name: str = Field(None, description="环境名")
    created_by_name: str = Field(None, description="创建人")


class EnvListSchema(BaseModel):
    """环境序列化"""
    name: str
    url: str = Field(None, description="url")
    remarks: str = Field(None, description="备注")


class EnvId(BaseModel):
    """环境序列化"""
    id: int = Field(..., description="id")


class EnvIdIn(BaseModel):
    """环境序列化"""
    env_id: int = Field(..., description="env_id")


class EnvIn(BaseModel):
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    domain_name: str = Field(None, description="")
    remarks: str = Field(None, description="")
    headers: typing.List[typing.Dict] = Field(None, description="")
    variables: typing.List[typing.Dict] = Field(None, description="")
    data_sources: typing.List[int] = Field(None, description="")


class BindingDataSourceIn(BaseModel):
    env_id: int = Field(..., description="")
    data_source_ids: typing.List[int] = Field(..., description="")


class BindingDataSourceId(BaseModel):
    id: int = Field(..., description="")


class BindingFuncIn(BaseModel):
    env_id: int = Field(..., description="")
    func_ids: typing.List[int] = Field(..., description="")


class BindingFuncId(BaseModel):
    func_id: int = Field(..., description="")
