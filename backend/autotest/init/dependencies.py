# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import Request
from autotest.corelibs import g


async def set_global_request(request: Request):
    """设置全局request 便与上下文的访问"""
    g.request = request
