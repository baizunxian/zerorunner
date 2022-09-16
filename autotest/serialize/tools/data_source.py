# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 17:01
from typing import Optional, Text
from autotest.serialize.base_serialize import BaseListSchema


class DataSourceListSchema(BaseListSchema):
    """菜单序列化"""
    type: Optional[Text]
    name: Optional[Text]
    host: Optional[Text]
    port: Optional[Text]
