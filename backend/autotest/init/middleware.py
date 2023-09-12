# -*- coding: utf-8 -*-
# @author: xiaobai
import time

from fastapi import FastAPI, Request
from loguru import logger
from config import config
from autotest.utils.local import g
from autotest.utils.consts import TEST_USER_INFO, CACHE_DAY
from autotest.utils.response.http_response import partner_success
from autotest.exceptions.exceptions import AccessTokenFail
from autotest.utils.common import get_str_uuid


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


def init_middleware(app: FastAPI):
    """"""

    @app.middleware("http")
    async def intercept(request: Request, call_next):
        g.trace_id = get_str_uuid()
        start_time = time.time()
        token = request.headers.get("token", None)
        g.redis = app.state.redis
        g.token = token
        remote_addr = request.headers.get("X-Real-IP", request.client.host)
        logger.info(f"访问记录:IP:{remote_addr}-method:{request.method}-url:{request.url}")
        # 登录校验
        try:
            await login_verification(request)
        except AccessTokenFail as err:
            return partner_success(code=err.code, msg=err.msg)
        response = await call_next(request)
        response.headers["X-request-id"] = g.trace_id
        return response
