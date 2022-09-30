# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

class Headers:
    """头信息处理"""

    def __init__(self):
        self.headers = {}

    def set(self, key, value):
        self.headers[key] = value

    def get(self, key):
        if hasattr(self.headers, key):
            return self.headers[key]
        return None

    def get_headers(self):
        return self.headers


class Environment:
    """环境变量处理"""

    def __init__(self):
        self.environment = {}

    def set(self, key, value):
        self.environment[key] = value

    def get(self, key):
        if hasattr(self.environment, key):
            return self.environment[key]
        return None

    def get_environment(self):
        return self.environment


class Zero:
    def __init__(self):
        self.headers = Headers()
        self.environment = Headers()


zero = Zero()
