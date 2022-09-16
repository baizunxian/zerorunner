import traceback

from flask import Flask, request
from loguru import logger

from autotest.corelibs.bredis import br
from autotest.exc import codes
from autotest.exc.consts import TEST_USER_INFO, CACHE_DAY
from autotest.exc.partner_message import partner_errmsg
from autotest.utils.api import partner_success, http_fail

white_router = [
    "/api/user/login",
    "/api/user/logout"
]


def init_middleware(app: Flask):
    app.before_request(login_verification)
    app.before_request(json_required)
    app.register_error_handler(Exception, exceptions)


def login_verification():
    """登录校验"""
    path = request.path
    if path and path not in white_router:
        token = request.headers.get('token', None)
        if not token:
            return partner_success(code=codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL,
                                   msg=partner_errmsg.get(codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL))
        user_info = br.get(TEST_USER_INFO.format(token))
        if not user_info:
            return partner_success(code=codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL,
                                   msg=partner_errmsg.get(codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL))
        # 重置token时间
        br.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)


def exceptions(err):
    """全局错误拦截"""
    logger.error(traceback.format_exc())
    return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


def json_required():
    """
    此装饰器可以装饰所有post请求 避免处理非json数据报错
    """
    if request.method == 'POST' and not request.is_json:
        logger.error(f'{request.path} json is required')
        return http_fail(code=codes.PARTNER_CODE_FAIL, msg='json is required')
