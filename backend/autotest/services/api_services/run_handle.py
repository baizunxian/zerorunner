# -*- coding: utf-8 -*-
# @author: xiaobai
from typing import List, Dict, Text, Any, Union

from autotest.models.api_models import ApiCase, Env
from autotest.models.tools_models import DataSource
from autotest.serialize.api_serializes.api_case import ApiCaseSchema, StepTypeEnum, \
    ApiCaseBaseSchema
from autotest.serialize.api_serializes.api_suites import ApiSuitesSchema
from autotest.utils.api import jsonable_encoder
from zerorunner.loader import load_module_functions
from zerorunner.models import TStep, TConfig, TRequest, TStepController
from zerorunner.parser import parse_string_value


def handle_step(step_data: List[Dict[Text, Any]]) -> Union[TStep, TStepController]:
    """ 处理对应的步骤转变为对应的控制器对象

    sql : SqlController    sql 控制器
    wait : WaitController  等待控制器
    case : TStep    用例
    extract : ExtractController  提取控制器
    script : ScriptController   脚本控制器

    """
    for step in step_data:
        step_type = step.get("step_type", None)
        controller = TStepController(**step)
        if step_type == StepTypeEnum.sql.value:
            source_info = DataSource.get(controller.source_id)
            if source_info:
                controller.host = source_info.host
                controller.user = source_info.user
                controller.password = source_info.password
                controller.port = source_info.port
        if step_type == StepTypeEnum.case.value:
            case_id = step.get("value", None)
            case_info = ApiCase.get(case_id)
            if case_info:
                controller = ApiCaseHandle(**jsonable_encoder(case_info)).step
        yield controller


def handle_headers_or_validators(param: List[ApiCaseBaseSchema]) -> Dict[Text, Any]:
    """处理请求头，跟变量
    args  param List[ApiCaseBaseSchema] 对象
    [
        {
        "key": "test",
        "value": "test_value",
        "remarks": "测试",
        }
    ]

    return
    {
        "test": "test_value"
    }

    """
    data = {}
    if not param:
        return data
    for p in param:
        data[p.key] = p.value
    return data


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
        self.make_functions()

    def make_functions(self):
        from autotest.utils import basic_function
        self.config.functions.update(load_module_functions(basic_function))

    def make_env(self):
        if self.api_case.env_id:
            env_info = Env.get(self.api_case.env_id)
            if env_info:
                ...

    def make_headers(self):
        headers = handle_headers_or_validators(self.api_case.headers)
        self.step.request.headers.update(headers)

    def make_request_body(self):
        self.step.request.data = self.api_case.request_body.data

    def make_variables(self):
        variables = handle_headers_or_validators(self.api_case.variables)
        self.step.variables.update(variables)

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
        headers = handle_headers_or_validators(self.api_suites.headers)
        self.config.headers.update(headers)

    def make_variables(self):
        variables = handle_headers_or_validators(self.api_suites.variables)
        self.config.variables.update(variables)
