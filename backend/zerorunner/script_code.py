# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from zerorunner.response import ResponseObject


class Zero:
    def __init__(self, request: dict = None, response: ResponseObject = None, environment: dict = None,
                 variables: dict = None):
        self.request = self.Request(request)
        self.response = self.Response(response)
        self.environment = self.Environment(environment)
        self.variables = self.Variables(variables)

    def __getattr__(self, item: str):
        if item == "request":
            return self.request
        if item == "response":
            return self.response
        elif item == "environment":
            return self.environment
        elif item == "variables":
            return self.variables
        else:
            raise AttributeError(f"{item} not found")

    class Request:
        """请求处理"""

        # {}.get()
        def __init__(self, request: dict = None):
            self.request = request if request else {}

        def __getattr__(self, item: str):
            if item in self.request:
                if isinstance(self.request[item], dict):
                    self.request[item] = CustomDict(self.request[item])
                    return self.request[item]
                return self.request[item]
            else:
                raise AttributeError(f"{item} not found in zero.request")

        def set(self, key, value):
            self.request[key] = value

        def get(self, key):
            if hasattr(self.request, key):
                return getattr(self.request, key)
            else:
                raise AttributeError(f"{key} not found in zero.request")

        def get_request(self):
            return self.request

    class Response:
        """响应处理"""

        def __init__(self, response: dict = None):
            self.response = response if response else {}

        def set(self, key, value):
            self.response[key] = value

        def get(self, key):
            if hasattr(self.response, key):
                return getattr(self.response, key)
            else:
                raise AttributeError(f"{key} not found in zero.response")

        def get_response(self):
            return self.response

    class Environment:
        """环境变量处理"""

        def __init__(self, environment: dict = None):
            self.environment = environment if environment else {}

        def __getattr__(self, item: str):
            if item in self.environment:
                if isinstance(self.environment[item], dict):
                    self.environment[item] = CustomDict(self.environment[item])
                    return self.environment[item]
                return self.environment[item]
            else:
                raise AttributeError(f"{item} not found in zero.environment")

        def set(self, key, value):
            self.environment[key] = value

        def get(self, key):
            if hasattr(self.environment, key):
                return getattr(self.environment, key)
            else:
                raise AttributeError(f"{key} not found in zero.environment")

        def get_environment(self):
            return self.environment

    class Variables:
        """变量处理"""

        def __init__(self, variables: dict = None):
            self.variables = variables if variables else {}

        def __getattr__(self, item: str):
            if item in self.variables:
                if isinstance(self.variables[item], dict):
                    self.variables[item] = CustomDict(self.variables[item])
                    return self.variables[item]
                return self.variables[item]
            else:
                raise AttributeError(f"{item} not found in zero.variables")

        def set(self, key, value):
            self.variables[key] = value

        def get(self, key):
            if hasattr(self.variables, key):
                return getattr(self.variables, key)
            else:
                raise AttributeError(f"{key} not found in zero.variables")

        def get_variables(self):
            return self.variables


class CustomDict(dict):

    def set(self, key, value):
        self[key] = value
