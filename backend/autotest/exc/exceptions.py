# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:48

class MyBaseFailure(Exception):
    pass


class ParameterError(MyBaseFailure):
    """参数错误"""
    pass
