# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from autotest.schemas.api.api_info import ApiInfoRun
from zerorunner.models import TController, TConfig


class HandelStep(object):
    api_info: ApiInfoRun
    config: TConfig
    teststeps: typing.List
    step: TController

    @classmethod
    async def init(cls, params: ApiInfoRun) -> "ApiInfoHandle":
        cls.api_info: ApiInfoRun = params
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
        if cls.api_info.request_body.mode.lower() == 'raw':
            if cls.api_info.request_body.language.lower() == "json":
                try:
                    cls.step.request.req_json = json.loads(cls.api_info.request_body.data)
                except Exception as err:
                    logger.error(traceback.format_exc())
                    cls.step.request.data = cls.api_info.request_body.data
            else:
                cls.step.request.data = cls.api_info.request_body.data
        elif cls.api_info.request_body.mode.lower() == 'form_data':
            from_data_list = cls.api_info.request_body.data
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
