# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from zerorunner.models.step_model import TStep
from zerorunner.response import ResponseObject
from zerorunner.runner import SessionRunner


class CustomDict(dict):

    def __getattr__(self, item: str):
        if item in self:
            return self[item]
        return None

    def set(self, key, value):
        self[key] = value


class DataHandle:

    def __init__(self, data: typing.Any, extra: str = "allow"):
        """
        extra: allow 允许, forbid 禁止  ignore 忽略
       """
        self._data = data
        self._extra = extra

    def __getattr__(self, item: str):
        if isinstance(self._data, type):
            if hasattr(self._data, item):
                return getattr(self._data, item)
            else:
                return None
        elif isinstance(self._data, dict):
            if item in self._data:
                if isinstance(self._data[item], dict):
                    self._data[item] = CustomDict(self._data[item])
                    return self._data[item]
                return self._data[item]
            else:
                return None
        return None

    def __setattr__(self, key, value):
        if key in ["_data", "_extra"]:
            super(DataHandle, self).__setattr__(key, value)
        else:
            self.set(key, value)

    def get(self, key):
        if isinstance(self._data, type):
            if hasattr(self._data, key):
                return getattr(self._data, key)
            else:
                return None
        if isinstance(self._data, dict):
            if key in self._data:
                return self._data[key]
            else:
                return None
        return None

    def set(self, key, value):
        if isinstance(self._data, type):
            if self._extra == "allow":
                setattr(self._data, key, value)
            else:
                if hasattr(self._data, key):
                    setattr(self._data, key, value)
        if isinstance(self._data, dict):
            if self._extra == "allow":
                self._data[key] = value
            else:
                if key in self._data:
                    self._data[key] = value


class Zero:
    def __init__(self, runner: SessionRunner,
                 step: TStep,
                 environment: dict,
                 variables: dict,
                 request: dict = None,
                 response: ResponseObject = None):
        self._runner = runner
        self._step = step
        self._environment = environment
        self._variables = variables
        self._request = request
        self._response = response

    @property
    def runner(self) -> SessionRunner:
        return self._runner

    @property
    def step(self):
        return self._step

    @property
    def request(self):
        return DataHandle(self._request, extra="forbid")

    @property
    def response(self):
        return DataHandle(self._response)

    @property
    def environment(self):
        return DataHandle(self._environment)

    @property
    def variables(self):
        return DataHandle(self._variables)
