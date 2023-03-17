# -*- coding: utf-8 -*-
# @author: xiaobai

from fastapi import FastAPI

from autotest.apis import app_router
from autotest.config import config


def register_router(app: FastAPI):
    """ 注册路由 """
    # 权限(权限在每个接口上)
    app.include_router(app_router, prefix=config.API_PREFIX)
