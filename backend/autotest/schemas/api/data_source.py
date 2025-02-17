import typing

from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema


class SourceQuery(BaseSchema):
    id: int = Field(None, description="id")
    source_type: str = Field("mysql", description="数据源类型")
    name: str = Field(None, description="")
    source_ids: typing.List[int] = Field(None, description="")


class SourceIn(BaseModel):
    id: int = Field(None, description="id")
    type: str = Field(None, description="数据源类型 mysql, redis, 等")
    name: str = Field(..., description="数据源名称")
    host: str = Field(None, description="地址")
    port: str = Field(None, description="端口")
    user: str = Field(None, description="用户名")
    password: str = Field(None, description="密码")


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
    name: str = Field(None, description="环境名称")
    domain_name: str = Field(None, description="域名")
    remarks: str = Field(None, description="备注")
    headers: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="请求头")
    variables: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="变量")
    data_sources: typing.List[int] = Field(None, description="数据源 弃用")
