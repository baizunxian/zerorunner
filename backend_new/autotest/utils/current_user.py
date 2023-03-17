# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from autotest.corelibs import g
from autotest.corelibs.consts import TEST_USER_INFO
from autotest.exceptions import AccessTokenFail


async def current_user(token: str) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
    """根据token获取用户信息"""
    user_info = await g.redis.get(TEST_USER_INFO.format(token))
    if not user_info:
        raise AccessTokenFail()
    return user_info
