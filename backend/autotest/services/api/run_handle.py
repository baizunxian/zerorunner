# -*- coding: utf-8 -*-
# @author: xiaobai
import json
import os
import traceback
import typing

from loguru import logger

from autotest.models.api_models import ApiInfo, Env, DataSource
from autotest.models.system_models import FileInfo
from autotest.schemas.api.api_case import TestCaseRun
from autotest.schemas.api.api_info import ApiInfoRun, ApiBaseSchema
from autotest.utils.serialize import default_serialize
from config import config
from zerorunner.loader import load_module_functions
from zerorunner.models import (
    TApiController,
    TConfig,
    TRequest,
    TSqlController,
    TScriptController,
    TWaitController,
    TIFController,
    TLoopController,
    TController, TestCase
)
from zerorunner.parser import parse_string_value


class HandleData(object):

    @staticmethod
    async def handle_functions(config: TConfig):
        from autotest.utils import basic_function
        config.functions.update(load_module_functions(basic_function))

    @staticmethod
    async def handle_env(env_id: typing.Union[str, int]) -> typing.Dict:
        env_dict = {}
        env_info = await Env.get(env_id)
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
    async def handle_step(step_data: typing.List[TController]) -> typing.List[TController]:
        """ 处理对应的步骤转变为对应的控制器对象

        sql : SqlController    sql 控制器
        wait : WaitController  等待控制器
        case : TStep    用例
        extract : ExtractController  提取控制器
        db_script : ScriptController   脚本控制器

        """
        steps = []
        for step in step_data:
            controller = None
            if isinstance(step, TApiController):
                case_info = await ApiInfo.get(step.case_id)
                if case_info:
                    case_info_dict = step.dict()
                    case_info_dict.update(default_serialize(case_info))
                    controller = (await ApiInfoHandle.init(ApiInfoRun(**case_info_dict))).step

            if isinstance(step, TSqlController):
                controller = step
                source_info = await DataSource.get(controller.source_id)
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
                controller.teststeps = await HandleData.handle_step(teststeps)

            if isinstance(step, TLoopController):
                controller = step
                teststeps = step.teststeps
                controller.teststeps = await HandleData.handle_step(teststeps)

            if controller:
                steps.append(controller)
        return steps

    @staticmethod
    def handle_headers_or_validators(param: typing.List[ApiBaseSchema]) -> typing.Dict:
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
    api_info: ApiInfoRun = None
    config: TConfig = None
    teststeps: typing.List = []
    step: TController = None

    @classmethod
    async def init(cls, params: ApiInfoRun) -> "ApiInfoHandle":
        cls.api_info: ApiInfoRun = None
        cls.config: TConfig = None
        cls.teststeps: typing.List = []
        cls.step: TController = None

        cls.api_info = params
        cls.config = TConfig(name=cls.api_info.name, case_id=cls.api_info.id)
        cls.teststeps = []
        cls.step = TApiController(
            enable=cls.api_info.enable,
            case_id=cls.api_info.id,
            index=cls.api_info.index,
            name=cls.api_info.name,
            request=TRequest(
                name=cls.api_info.name,
                url=cls.api_info.url,
                method=cls.api_info.method
            ),
            extracts=cls.api_info.extracts

        )
        await cls.make_env()
        await cls.make_headers(HandleData.handle_headers_or_validators(cls.api_info.headers))
        await cls.make_request_body()
        await cls.make_variables(HandleData.handle_headers_or_validators(cls.api_info.variables), "var")
        await cls.make_setup_hooks()
        await cls.make_teardown_hooks()
        await cls.make_validators()
        # await cls.make_functions()

        cls.teststeps.append(cls.step)

        return cls

    @classmethod
    async def make_functions(cls):
        await HandleData.handle_functions(cls.config)

    @classmethod
    async def make_env(cls):
        if cls.api_info.env_id:
            env_info = await HandleData.handle_env(cls.api_info.env_id)
            cls.config.base_url = env_info.get("base_url")
            await cls.make_variables(env_info.get("variables", {}), "env_var")
            await cls.make_headers(env_info.get("headers", {}))

    def make_step(self):
        ...

    @classmethod
    async def make_headers(cls, headers: typing.Dict):
        cls.step.request.headers.update(headers)

    @classmethod
    async def make_request_body(cls):
        if cls.api_info.request.mode.lower() == 'raw':
            if cls.api_info.request.language.lower() == "json":
                try:
                    cls.step.request.req_json = json.loads(cls.api_info.request.data)
                except Exception as err:
                    logger.error(traceback.format_exc())
                    cls.step.request.data = cls.api_info.request.data
            else:
                cls.step.request.data = cls.api_info.request.data
        elif cls.api_info.request.mode.lower() == 'form_data':
            from_data_list = cls.api_info.request.data
            upload_dict = {}
            for data in from_data_list:
                if data.type == "file":
                    file_value_info = data.value
                    file_info = await FileInfo.get(file_value_info.id)
                    if not file_info:
                        logger.error(f"文件不存在：{file_value_info.id}")
                        raise PermissionError("文件不存在！")
                    abs_file_path = os.path.join(config.TEST_FILES_DIR, file_info.name)
                    if not os.path.exists(abs_file_path):
                        logger.error(f"文件找不到：{file_info.name}")
                        raise FileNotFoundError(f'文件 {file_info.name} 找不到~')
                    upload_dict[data.key] = abs_file_path
                else:
                    upload_dict[data.key] = data.value
            cls.step.request.upload = upload_dict

    @classmethod
    async def make_variables(cls, variables: typing.Dict, var_type: str):
        """
        变量处理
        args ->
         variables : 变量
         var_type : 变量类型
        """
        if var_type == "var":
            # 用例变量
            cls.step.variables.update(variables)
            cls.step.variables = {key: parse_string_value(value) for key, value in cls.step.variables.items()}
        if var_type == "env_var":
            # 全局变量
            cls.config.env_variables.update(variables)
            cls.config.env_variables = {key: parse_string_value(value) for key, value in
                                        cls.config.env_variables.items()}

    @classmethod
    async def make_setup_hooks(cls):
        for step in await HandleData.handle_step(cls.api_info.setup_hooks):
            cls.step.setup_hooks.append(step)

    @classmethod
    async def make_teardown_hooks(cls):
        for step in await HandleData.handle_step(cls.api_info.teardown_hooks):
            cls.step.teardown_hooks.append(step)

    @classmethod
    async def make_validators(cls):
        if cls.api_info.validators and isinstance(cls.api_info.validators, typing.List):
            for vail in cls.api_info.validators:
                vail.expect = parse_string_value(vail.expect)
                cls.step.validators.append(vail.dict())

    @classmethod
    def get_testcase(cls) -> "TestCase":
        return TestCase(config=cls.config, teststeps=cls.teststeps)


class ApiCaseHandle:
    api_case: TestCaseRun = None
    config: TConfig = None
    teststeps: typing.List = []

    @classmethod
    async def init(cls, api_case: TestCaseRun):
        cls.api_case = None
        cls.config = None
        cls.teststeps = []
        cls.api_case = api_case
        cls.config = TConfig(name=cls.api_case.name, case_id=cls.api_case.id)
        await cls.make_env()
        await cls.make_testcase()
        # await cls.make_functions()
        await cls.make_headers(HandleData.handle_headers_or_validators(cls.api_case.headers))
        await cls.make_variables(HandleData.handle_headers_or_validators(cls.api_case.variables), 'var')
        return cls

    @classmethod
    async def make_functions(cls):
        await HandleData.handle_functions(cls.config)

    @classmethod
    async def make_env(cls):
        if cls.api_case.env_id:
            env_info = await HandleData.handle_env(cls.api_case.env_id)
            cls.config.base_url = env_info.get("base_url", "")
            await cls.make_headers(env_info.get("headers", {}))
            await cls.make_variables(env_info.get("variables", {}), "env_var")

    @classmethod
    async def make_testcase(cls):
        for step in await HandleData.handle_step(cls.api_case.step_data):
            cls.teststeps.append(step)

    @classmethod
    async def make_headers(cls, headers: typing.Dict):
        cls.config.headers.update(headers)

    @classmethod
    async def make_variables(cls, variables: typing.Dict, var_type: str):
        if var_type == "env_var":
            cls.config.env_variables.update(variables)
            cls.config.env_variables = {key: parse_string_value(value) for key, value in
                                        cls.config.env_variables.items()}
        if var_type == "var":
            cls.config.variables.update(variables)
            cls.config.variables = {key: parse_string_value(value) for key, value in cls.config.variables.items()}

    @classmethod
    def get_testcase(cls) -> "TestCase":
        testcase = TestCase(config=cls.config, teststeps=cls.teststeps)
        return testcase
