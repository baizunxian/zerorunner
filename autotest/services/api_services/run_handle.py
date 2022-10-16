# -*- coding: utf-8 -*-
# @author: xiaobai
import ast
from typing import List, Dict, Text, Any

from autotest.models.api_models import ApiCase
from autotest.models.tools_models import DataSource
from autotest.serialize.api_serializes.api_case import ApiCaseValidatorsSchema, ApiCaseSchema, StepTypeEnum
from autotest.serialize.api_serializes.api_suites import ApiSuitesSchema
from autotest.utils.api import jsonable_encoder
from zerorunner.models import TStep, TConfig, TRequest, SqlController, WaitController, ExtractController, \
    ScriptController
from zerorunner.parser_param import parse_string_value


def handle_step(step_data: List[Dict[Text, Any]]):
    for step in step_data:
        controller = None
        step_type = step.get("step_type", None)
        if step_type == StepTypeEnum.sql.value:
            controller = SqlController(**step)
            source_info = DataSource.get(controller.source_id)
            if source_info:
                controller.host = source_info.host
                controller.user = source_info.user
                controller.password = source_info.password
                controller.port = source_info.port

        if step_type == StepTypeEnum.wait.value:
            controller = WaitController(**step)

        if step_type == StepTypeEnum.case.value:
            case_id = step.get("value", None)
            case_info = ApiCase.get(case_id)
            if case_info:
                zr = ApiCaseHandle(**jsonable_encoder(case_info))
                controller = zr.step
        if step_type == StepTypeEnum.extract.value:
            controller = ExtractController(**step)

        if step_type == StepTypeEnum.script.value:
            controller = ScriptController(**step)

        yield controller


class ApiCaseHandle(object):

    def __init__(self, **kwargs: Any):
        self.api_case = ApiCaseSchema(**kwargs)
        self.config = TConfig(name=self.api_case.name)
        self.step = TStep(
            name=self.api_case.name,
            request=TRequest(
                name=self.api_case.name,
                url=self.api_case.url,
                method=self.api_case.method
            )
        )
        self.make_headers()
        self.make_request_body()
        self.make_variables()
        self.make_setup_hooks()
        self.make_teardown_hooks()
        self.make_validators()

    def make_headers(self):
        headers_dict = {}
        for head in self.api_case.headers:
            headers_dict[head.key] = head.value
        self.step.request.headers.update(headers_dict)

    def make_request_body(self):
        self.step.request.data = self.api_case.request_body.data

    def make_variables(self):
        variables_dict = {}
        for variable in self.api_case.variables:
            variables_dict[variable.key] = parse_string_value(variable.value)
        self.step.variables.update(variables_dict)

    def make_setup_hooks(self):
        for step in handle_step(self.api_case.setup_hooks):
            self.step.setup_hooks.append(step)

    def make_teardown_hooks(self):
        for step in handle_step(self.api_case.teardown_hooks):
            self.step.teardown_hooks.append(step)

    def make_validators(self):
        for vail in self.api_case.validators:
            vail.expect = parse_string_value(vail.expect)
            self.step.validators.append(vail.dict())


class ApiSuiteHandle:

    def __init__(self, **kwargs: Any):
        self.api_suites = ApiSuitesSchema(**kwargs)
        self.config = TConfig(name=self.api_suites.name)
        self.teststeps = []
        self.make_step()
        self.make_headers()
        self.make_variables()

    def make_step(self):
        for step in handle_step(self.api_suites.step_data):
            self.teststeps.append(step)

    def make_headers(self):
        headers_dict = {}
        for head in self.api_suites.headers:
            headers_dict[head.key] = head.value
        self.config.headers.update(headers_dict)

    def make_variables(self):
        variables_dict = {}
        for variable in self.api_suites.variables:
            variables_dict[variable.key] = variable.value
        self.config.variables.update(variables_dict)
