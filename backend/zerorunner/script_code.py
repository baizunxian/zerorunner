# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from zerorunner.model.step_model import TStep
from zerorunner.response import ResponseObject
from zerorunner.runner import SessionRunner


class Zero:
    def __init__(self, runner: SessionRunner,
                 step: TStep,
                 request: dict = None,
                 response: ResponseObject = None,
                 environment: dict = None,
                 variables: dict = None):
        self._runner = runner
        self._step = step
        self._request = request
        self._response = response
        self._environment = environment
        self._variables = variables

    @property
    def runner(self) -> SessionRunner:
        return self._runner

    @property
    def step(self):
        return self._step

    @property
    def request(self):
        return self.Request(self._request)

    @property
    def response(self):
        return self.Response(self._response)

    @property
    def environment(self):
        return self.Environment(self._environment)

    @property
    def variables(self):
        return self.Variables(self._variables)

    class Request:
        """请求处理"""

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

        def get_headers(self):
            return self.request.get("headers")

        def get_json(self):
            return self.request.get("json")

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
