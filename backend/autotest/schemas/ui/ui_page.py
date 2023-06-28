# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field


class UiPageQuery(BaseModel):
    """页面查询条件"""
    id: int = Field(None, title="页面id")
    name: str = Field(None, title="页面名称")
    url: str = Field(None, title="页面地址")


class UiPageIn(BaseModel):
    """页面入参"""
    id: int = Field(None, title="id")
    name: str = Field(..., title="页面名称")
    url: str = Field(..., title="页面地址")
    project_id: int = Field(..., title="项目id")
    module_id: int = Field(..., title="模块id")
    remarks: str = Field(None, title="备注")
    tags: typing.List = Field(None, title="备注")


class UiPageId(BaseModel):
    id: int = Field(..., title="id")
