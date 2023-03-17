# -*- coding: utf-8 -*-
# @author: xiaobai
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from autotest.config import config
from autotest.corelibs import g
from autotest.corelibs import logger
from autotest.corelibs.codes import CodeEnum
from autotest.corelibs.consts import TEST_USER_INFO, CACHE_DAY
from autotest.corelibs.http import partner_success
from autotest.exceptions import AccessTokenFail


def register_cors(app: FastAPI):
    """ 跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/ """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )


async def set_body(request: Request):
    """设置请求体"""
    receive_ = await request._receive()

    async def receive():
        return receive_

    request._receive = receive


async def login_verification(request: Request):
    """
    登录校验
    :param request: 路径
    :return:
    """
    token = request.headers.get("token", None)
    router: str = request.scope.get('path', "")
    if router.startswith("/api") and not router.startswith("/api/file") and router not in config.WHITE_ROUTER:
        if not token:
            raise AccessTokenFail()
        user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise AccessTokenFail()
        # 重置token时间
        await g.redis.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def intercept(request: Request, call_next):
        token = request.headers.get("token", None)
        await set_body(request)
        g.redis = app.state.redis
        g.request = request
        g.token = token
        logger.info(f"访问记录:IP:{request.client.host}-method:{request.method}-url:{request.url}")
        # 登录校验
        try:
            await login_verification(request)
        except AccessTokenFail as err:
            return partner_success(code=err.code, msg=err.msg)
        response = await call_next(request)
        response.headers["X-request-id"] = g.trace_id
        return response
