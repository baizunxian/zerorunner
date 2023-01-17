# -*- coding: utf-8 -*-
# @author: xiaobai
from typing import List, Dict, Text, Any, Union

from autotest.models.api_models import ApiInfo, Env
from autotest.models.tools_models import DataSource
from autotest.serialize.api_serializes.api_info import ApiInfoSchema, \
    ApiBaseSchema
from autotest.serialize.api_serializes.api_case import ApiCaseSchema
from autotest.utils.api import jsonable_encoder
from zerorunner.loader import load_module_functions
from zerorunner.models import (
    TCaseController,
    TConfig,
    TRequest,
    TSqlController,
    TScriptController,
    TWaitController,
    TIFController,
    TLoopController,
    TController, TestCase, TestSuite
)
from zerorunner.parser import parse_string_value
from zerorunner.runner import Runner


class HandleData(object):

    @staticmethod
    def handle_functions(config: TConfig):
        from autotest.utils import basic_function
        config.functions.update(load_module_functions(basic_function))

    @staticmethod
    def handle_env(env_id: Union[Text, int]) -> Dict[Text, Any]:
        env_dict = {}
        env_info = Env.get(env_id)
        if env_info:
            # 环境初始化
            domain_name = env_info.domain_name
            env_headers = env_info.headers
            env_variables = env_info.variables
            # 环境域名
            if domain_name:
                env_dict["base_url"] = domain_name
            # 环境请求头
            if env_headers:
                env_dict["headers"] = HandleData.handle_headers_or_validators(env_headers)
            # 环境变量
            if env_variables:
                env_dict["variables"] = HandleData.handle_headers_or_validators(env_variables)
        return env_dict

    @staticmethod
    def handle_step(step_data: List[TController]) -> List[TController]:
        """ 处理对应的步骤转变为对应的控制器对象

        sql : SqlController    sql 控制器
        wait : WaitController  等待控制器
        case : TStep    用例
        extract : ExtractController  提取控制器
        script : ScriptController   脚本控制器

        """
        steps = []
        for step in step_data:
            controller = None
            if isinstance(step, TCaseController):
                case_info = ApiInfo.get(step.case_id)
                if case_info:
                    case_info_dict = step.dict()
                    case_info_dict.update(jsonable_encoder(case_info))
                    controller = ApiInfoHandle(**case_info_dict).step

            if isinstance(step, TSqlController):
                controller = step
                source_info = DataSource.get(controller.source_id)
                if source_info:
                    controller.host = source_info.host
                    controller.user = source_info.user
                    controller.password = source_info.password
                    controller.port = source_info.port

            if isinstance(step, TWaitController):
                controller = step

            if isinstance(step, TScriptController):
                controller = step

            if isinstance(step, TIFController):
                controller = step
                teststeps = step.teststeps
                controller.teststeps = HandleData.handle_step(teststeps)

            if isinstance(step, TLoopController):
                controller = step
                teststeps = step.teststeps
                controller.teststeps = HandleData.handle_step(teststeps)

            if controller:
                steps.append(controller)
        return steps

    @staticmethod
    def handle_headers_or_validators(param: List[ApiBaseSchema]) -> Dict[Text, Any]:
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
            if isinstance(p, dict):
                p = ApiBaseSchema(**p)
            data[p.key] = p.value
        return data


class ApiInfoHandle(object):

    def __init__(self, **kwargs: Any):
        self.api_info = ApiInfoSchema(**kwargs)
        self.config = TConfig(name=self.api_info.name)
        self.teststeps = []
        self.step = TCaseController(
            step_type="case",
            enable=self.api_info.enable,
            case_id=self.api_info.id,
            index=self.api_info.index,
            name=self.api_info.name,
            request=TRequest(
                name=self.api_info.name,
                url=self.api_info.url,
                method=self.api_info.method
            ),
            extracts=self.api_info.extracts

        )
        self.make_env()
        self.make_headers(HandleData.handle_headers_or_validators(self.api_info.headers))
        self.make_request_body()
        self.make_variables(HandleData.handle_headers_or_validators(self.api_info.variables), "var")
        self.make_setup_hooks()
        self.make_teardown_hooks()
        self.make_validators()
        self.make_functions()
        self.teststeps.append(self.step)

    def make_functions(self):
        HandleData.handle_functions(self.config)

    def make_env(self):
        env_info = HandleData.handle_env(self.api_info.env_id)
        self.config.base_url = env_info.get("base_url")
        self.make_headers(env_info.get("headers", {}))
        self.make_variables(env_info.get("variables", {}), "env_var")

    def make_step(self):
        ...

    def make_headers(self, headers: Dict[Text, Text]):
        self.step.request.headers.update(headers)

    def make_request_body(self):
        self.step.request.data = self.api_info.request_body.data

    def make_variables(self, variables: Dict[Text, Text], var_type: Text):
        """
        变量处理
        args ->
         variables : 变量
         var_type : 变量类型
        """
        if var_type == "var":
            # 用例变量
            self.step.variables.update(variables)
        if var_type == "env_var":
            # 全局变量
            self.config.env_variables.update(variables)

    def make_setup_hooks(self):
        for step in HandleData.handle_step(self.api_info.setup_hooks):
            self.step.setup_hooks.append(step)

    def make_teardown_hooks(self):
        for step in HandleData.handle_step(self.api_info.teardown_hooks):
            self.step.teardown_hooks.append(step)

    def make_validators(self):
        if self.api_info.validators and isinstance(self.api_info.validators, List):
            for vail in self.api_info.validators:
                vail.expect = parse_string_value(vail.expect)
                self.step.validators.append(vail.dict())

    def get_testcase(self) -> "TestCase":
        return TestCase(config=self.config, teststeps=self.teststeps)


class ApiCaseHandle:

    def __init__(self, **kwargs: Any):
        """
        kwargs: -> suites info
        """
        self.api_case = ApiCaseSchema(**kwargs)
        self.config = TConfig(name=self.api_case.name)
        self.teststeps = []
        self.make_testcase()
        self.make_functions()
        self.make_headers(HandleData.handle_headers_or_validators(self.api_case.headers))
        self.make_variables(HandleData.handle_headers_or_validators(self.api_case.variables), 'var')

    def make_functions(self):
        HandleData.handle_functions(self.config)

    def make_env(self):
        if self.api_case.env_id:
            env_info = HandleData.handle_env(self.api_case.env_id)
            self.config.base_url = env_info.get("base_url", "")
            self.make_headers(env_info.get("headers", {}))
            self.make_variables(env_info.get("variables", {}), "env_var")

    def make_testcase(self):
        for step in HandleData.handle_step(self.api_case.step_data):
            self.teststeps.append(step)

    def make_headers(self, headers: Dict[Text, Text]):
        self.config.headers.update(headers)

    def make_variables(self, variables: Dict[Text, Text], var_type: Text):
        if var_type == "env_var":
            self.config.env_variables.update(variables)
        if var_type == "var":
            self.config.variables.update(variables)

    def get_testcase(self) -> "TestCase":
        return TestCase(config=self.config, teststeps=self.teststeps)


class Runner(object):
    def __init__(self, testcase: TestCase):
        self.zr = Runner()
        self.testcase = testcase

    def run(self):
        self.zr.run_testcase(self.testcase)

    def get_summary(self):
        return self.zr.get_summary()
