# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel, Field


class UiElementQuery(BaseModel):
    """页面元素查询条件"""
    name: str = Field(None, title="元素名称")
    page_id: str = Field(None, title="页面id")


class UiElementIn(BaseModel):
    """页面元素入参"""
    id: int = Field(None, title="id")
    name: str = Field(..., title="元素名称")
    location_method: str = Field(..., title="定位方式")
    location_value: str = Field(..., title="定位值")
    page_id: int = Field(..., title="页面id")
    remarks: str = Field(None, title="备注")


class UiElementId(BaseModel):
    id: int = Field(..., title="id")
