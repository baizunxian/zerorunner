# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel, Field


class UiElementQuery(BaseModel):
    """页面元素查询条件"""
    name: str = Field(None, title="页面名称")


class UiElementIn(BaseModel):
    """页面元素入参"""
    id: int = Field(None, title="id")
    name: str = Field(..., title="页面名称")
    location_type: str = Field(..., title="定位方式")
    location_value: str = Field(..., title="定位值")
    page_id: int = Field(..., title="页面id")
    remark: str = Field(None, title="备注")
