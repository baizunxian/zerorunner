import time
from typing import Dict, Union

from flask import request
from loguru import logger

from autotest.corelibs.bredis import br
from autotest.exc.consts import TEST_USER_INFO


def get_timestamp():
    """
    获取当前时间戳
    :return:
    """
    t = time.time()
    return str(round(t * 1000))


def get_user_info_by_token() -> Dict:
    """
    根据token获取用户信息
    :return:
    """
    try:
        token = request.headers.get('token')
        user_id = request.headers.get('userId', None)
    except RuntimeError as err:
        logger.debug(f'get user token err：{err}')
        return None
    user_info = br.get(TEST_USER_INFO.format(token))
    if user_info is None:
        if user_id:
            user_info = {'id': int(user_id)}
    return user_info


def get_user_id_by_token() -> Union[int, str]:
    """
    根据token获取用户信息
    :return:
    """
    return get_user_info_by_token().get('id')
