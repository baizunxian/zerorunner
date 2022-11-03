# -*- coding: utf-8 -*-
# @author: xiaobai

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


class Variables:
    """头信息处理"""

    def __init__(self):
        self.variables = {}

    def set(self, key, value):
        self.variables[key] = value

    def get(self, key):
        if hasattr(self.variables, key):
            return self.variables[key]
        return None

    def get_headers(self):
        return self.variables


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
        self.environment = Environment()
        self.variables = Variables()


zero = Zero()
