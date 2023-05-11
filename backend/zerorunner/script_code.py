# -*- coding: utf-8 -*-
# @author: xiaobai
import typing


class Zero:
    def __init__(self, headers: dict = None, environment: dict = None, variables: dict = None):
        self._headers = self.Headers(headers)
        self._environment = self.Environment(environment)
        self._variables = self.Variables(variables)

    @property
    def headers(self):
        return self._headers

    @property
    def environment(self):
        return self._environment

    @property
    def variables(self):
        return self._variables

    class Headers:
        def __init__(self, headers: dict = None):
            self.headers = headers if headers else {}

        def set(self, key, value):
            self.headers[key] = value

        def get(self, key):
            return self.headers.get(key, None)

        def get_headers(self):
            return self.headers

    class Environment:
        """环境变量处理"""

        def __init__(self, environment: dict = None):
            self.environment = environment if environment else {}

        def set(self, key, value):
            self.environment[key] = value

        def get(self, key):
            return self.environment.get(key, None)

        def get_environment(self):
            return self.environment

    class Variables:
        """头信息处理"""

        def __init__(self, variables: dict = None):
            self.variables = variables if variables else {}

        def set(self, key, value):
            self.variables[key] = value

        def get(self, key):
            return self.variables.get(key, None)

        def get_variables(self):
            return self.variables
