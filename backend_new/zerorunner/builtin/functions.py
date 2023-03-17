# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

"""
测试用例内置函数
"""

import datetime
import random
import string
import time

from zerorunner.exceptions import ParamsError


def gen_random_string(str_len):
    """ 获取随机字符串
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
    )


def get_timestamp(str_len=13):
    """ 获取时间戳
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")


def get_current_date(fmt="%Y-%m-%d"):
    """获取当前日期
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(n_secs):
    """ 睡眠 n 秒
    """
    time.sleep(n_secs)
