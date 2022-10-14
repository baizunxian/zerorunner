# -*- coding: utf-8 -*-
# @author: xiaobai
from typing import List, Dict, Text, Any

from autotest.models.api_models import ApiCase
from autotest.models.tools_models import DataSource
from autotest.serialize.api_serializes.api_case import ApiCaseValidatorsSchema, ApiCaseSchema, StepTypeEnum
from autotest.utils.api import jsonable_encoder
from zerorunner.models import TStep, TConfig, TRequest, SqlController, WaitController, ExtractController, \
    ScriptController


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
            variables_dict[variable.key] = variable.value
        self.step.variables.update(variables_dict)

    def make_setup_hooks(self):
        self.handle_hooks(self.api_case.setup_hooks, "setup")

    def make_teardown_hooks(self):
        self.handle_hooks(self.api_case.teardown_hooks, "teardown")

    def handle_hooks(self, hook: List[Dict[Text, Any]], hook_type: Text):
        for hook in hook:
            controller = None
            step_type = hook.get("step_type", None)
            if step_type == StepTypeEnum.sql.value:
                controller = SqlController(**hook)
                source_info = DataSource.get(controller.source_id)
                if source_info:
                    controller.host = source_info.host
                    controller.user = source_info.user
                    controller.password = source_info.password
                    controller.port = source_info.port

            if step_type == StepTypeEnum.wait.value:
                controller = WaitController(**hook)

            if step_type == StepTypeEnum.case.value:
                case_id = hook.get("value", None)
                case_info = ApiCase.get(case_id)
                if case_info:
                    zr = ApiCaseHandle(**jsonable_encoder(case_info))
                    controller = zr.step
            if step_type == StepTypeEnum.extract.value:
                controller = ExtractController(**hook)

            if step_type == StepTypeEnum.script.value:
                controller = ScriptController(**hook)

            if hook_type == "setup":
                self.step.setup_hooks.append(controller)
            elif hook_type == "teardown":
                self.step.teardown_hooks.append(controller)

    def make_validators(self):
        for vail in self.api_case.validators:
            self.step.validators.append(vail.dict())
