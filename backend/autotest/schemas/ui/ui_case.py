# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field


class UiCaseQuery(BaseModel):
    """用例查询条件"""
    name: str = Field(None, title="页面名称")


class UiCaseIn(BaseModel):
    """用例入参"""
    id: int = Field(None, title="id")
    name: str = Field(..., title="用例名称")
    project_id: int = Field(..., title="项目id")
    module_id: int = Field(..., title="模块id")
    tags: typing.List = Field(None, title="标签")
    setup_hooks: str = Field(None, title="前置条件")
    teardown_hooks: str = Field(None, title="后置条件")
    variables: typing.Dict = Field(None, title="变量")
    remarks: str = Field(None, title="备注")


class UiCaseId(BaseModel):
    id: int = Field(..., title="id")
