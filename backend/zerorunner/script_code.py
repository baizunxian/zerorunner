# -*- coding: utf-8 -*-
# @author: xiaobai
import typing


class ZHeaders:
    """头信息处理"""

    def __init__(self, headers: typing.Dict):
        self.headers = headers

    def set(self, key, value):
        self.headers[key] = value

    def get(self, key):
        if hasattr(self.headers, key):
            return self.headers[key]
        return None

    def get_headers(self):
        return self.headers


class ZVariables:
    """头信息处理"""

    def __init__(self, variables: typing.Dict):
        self.variables = variables

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

    def __init__(self, environment: typing.Dict):
        self.environment = environment

    def set(self, key, value):
        self.environment[key] = value

    def get(self, key):
        if hasattr(self.environment, key):
            return self.environment[key]
        return None

    def get_environment(self):
        return self.environment


class Zero:
    def __init__(self, request_dict: typing.Dict, environment: typing.Dict, variables: typing.Dict):
        self._headers = ZHeaders(request_dict.get("headers", {}))
        self._environment = Environment(environment)
        self._variables = ZVariables(variables)

    @property
    def headers(self):
        return self._headers

    @property
    def environment(self):
        return self._environment

    @property
    def variables(self):
        return self._variables
