# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import Request

from autotest.utils.local import g


async def set_global_request(request: Request):
    """设置全局request 便与上下文的访问"""
    g.request = request


# class LoginVerification:
#     async def __call__(self, token: str = Depends(APIKeyHeader(name="token"))):
#         if not token:
#             return partner_success(code=CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL,
#                                    msg=CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
#         return token


# async def login_verification(request: Request, token: Security = Security(LoginVerification())):
#     """
#     登录校验
#     :param request: 路径
#     :param token: token
#     :return:
#     """
#     if not token:
#         raise AccessTokenFail()
#     router: str = request.scope.get('path', "")
#     if router.startswith("/api") and not router.startswith("/api/file") and router not in config.WHITE_ROUTER:
#         user_info = await g.redis.get(TEST_USER_INFO.format(token))
#         if not user_info:
#             raise AccessTokenFail()
#         # 重置token时间
#         await g.redis.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)
