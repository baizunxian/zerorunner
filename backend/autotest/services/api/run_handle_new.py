# -*- coding: utf-8 -*-
# @author: xiaobai
import json
import os
import traceback
import typing
import uuid
from json.decoder import JSONDecodeError

from loguru import logger

from autotest.models.api_models import Env, DataSource, ApiInfo, EnvFunc
from autotest.models.system_models import FileInfo
from autotest.schemas.api.api_case import TestCaseRun, TCaseStepData
from autotest.schemas.api.api_info import ApiBaseSchema, ApiInfoIn
from autotest.schemas.step_data import TStepData
from autotest.utils.des import decrypt_rsa_password
from config import config
from zerorunner.loader import load_module_functions, load_func_content
from zerorunner.model.base import TStepTypeEnum
from zerorunner.model.step_model import TStep, TRequest, TSqlRequest, TIFRequest, TLoopRequest, TScriptRequest, \
    TWaitRequest, TestCase, TUiRequest, TConfig
from zerorunner.steps.step import Step
from zerorunner.steps.step_api_requet import RunRequestStep
from zerorunner.steps.step_if_requet import RunIFStep
from zerorunner.steps.step_loop_requet import RunLoopStep
from zerorunner.steps.step_script_requet import RunScriptStep
from zerorunner.steps.step_sql_request import RunSqlStep
from zerorunner.steps.step_ui_requet import RunUiStep
from zerorunner.steps.step_wait_requet import RunWaitStep


def parse_string_to_json(str_value: str):
    try:
        return json.loads(str_value)
    except TypeError:
        return str_value
    except JSONDecodeError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


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


def parse_validators_string_value(validators: typing.Dict):
    return {key: parse_string_to_json(value) for key, value in validators.items()}


class HandleConfig(object):
    config: TConfig

    async def init(self,
                   env_id: typing.Union[int, str],
                   case_id: typing.Union[int, str] = None,
                   headers: typing.List[ApiBaseSchema] = None,
                   variables: typing.List[ApiBaseSchema] = None) -> "HandleConfig":
        self.config = TConfig(name="", case_id=case_id)
        await self.init_env(env_id)
        await self.init_functions()
        if headers:
            await self.init_headers(headers)
        if variables:
            await self.init_variables(headers)

        return self

    async def init_env(self, env_id: typing.Union[int, str]):
        env_info = await Env.get(env_id)
        if env_info:
            # 环境初始化
            env_variables = env_info.variables
            # 环境域名
            if env_info.domain_name:
                self.config.base_url = env_info.domain_name

            # 环境变量
            if env_info.variables:
                new_variables = handle_headers_or_validators(env_variables)
                # 43 修复环境变量覆盖用例变量
                self.config.env_variables = parse_validators_string_value(new_variables)
            # 环境请求头
            if env_info.headers:
                self.config.headers.update(handle_headers_or_validators(env_info.headers))
        config_funcs = await EnvFunc.get_by_env_id(env_id) if env_id else []
        if config_funcs:
            for func in config_funcs:
                func_content = func.get("content", None)
                if func_content:
                    self.config.functions.update(
                        load_func_content(func_content, f"{func.get('name', '')}{uuid.uuid4().hex}"))

    async def init_headers(self, headers: typing.List[ApiBaseSchema]):
        self.config.headers.update(handle_headers_or_validators(headers))

    async def init_variables(self, variables: typing.List[ApiBaseSchema]):
        new_variables = handle_headers_or_validators(variables)
        self.config.variables.update(parse_validators_string_value(new_variables))

    async def init_functions(self):
        from autotest.utils import basic_function
        self.config.functions.update(load_module_functions(basic_function))


class HandleStepData(object):
    api_info: TStepData
    config: TConfig
    step: TStep = TStep()
    step_obj: typing.Union[Step, None] = None

    # 排除需要处理的参数

    async def init(self, params: TStepData) -> "HandleStepData":
        # 过滤需要处理的数据 其他参数一次性赋值给TStep对象
        exclude_set = {"request", "sql_request", "if_request", "loop_request", "wait_request", "script_request",
                       "ui_request", "variables", "setup_hooks", "teardown_hooks", "validators"}
        self.step = TStep(**params.dict(exclude=exclude_set))
        self.api_info = params
        self.step_obj = None
        await self.init_step()
        return self

    async def init_step(self):
        step_obj = None
        step_type = self.api_info.step_type.lower()
        self.step.step_type = self.api_info.step_type
        if step_type == TStepTypeEnum.api.value.lower():
            step_obj = await self.__init_api_step()
            await self.init_request_headers()
        elif step_type == TStepTypeEnum.sql.value.lower():
            step_obj = await self.__init_sql_step()
        elif step_type == TStepTypeEnum.wait.value.lower():
            step_obj = await self.__init_wait_step()
        elif step_type == TStepTypeEnum.loop.value.lower():
            step_obj = await self.__init_loop_step()
        elif step_type == TStepTypeEnum.IF.value.lower():
            step_obj = await self.__init_if_step()
        elif step_type == TStepTypeEnum.script.value.lower():
            step_obj = await self.__init_script_step()
        elif step_type == TStepTypeEnum.ui.value.lower():
            step_obj = await self.__init_ui_step()

        await self.init_variables()
        await self.init_setup_hooks()
        await self.init_teardown_hooks()
        await self.init_validators()
        self.step_obj = step_obj

    async def __init_api_step(self) -> Step:
        self.step.request = TRequest(method=self.api_info.request.method, url=self.api_info.request.url)
        request_mode = self.api_info.request.mode.lower()
        if request_mode == 'raw':
            if self.api_info.request.language.lower() == "json":
                try:
                    self.step.request.req_json = json.loads(self.api_info.request.data)
                except Exception:
                    logger.error(traceback.format_exc())
                    self.step.request.data = self.api_info.request.data
            else:
                self.step.request.data = self.api_info.request.data
        elif request_mode == 'form_data':
            from_data_list = self.api_info.request.data
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
            self.step.request.upload = upload_dict

        elif request_mode == 'none':
            self.step.request.data = None
        return Step(RunRequestStep(self.step))

    async def __init_ui_step(self) -> Step:
        self.step.ui_request = TUiRequest(**self.api_info.ui_request.dict())
        return Step(RunUiStep(self.step))

    async def __init_sql_step(self) -> Step:
        source_info = await DataSource.get(self.api_info.sql_request.source_id)
        self.step.sql_request = TSqlRequest(**self.api_info.sql_request.dict())
        if source_info:
            self.step.sql_request.host = source_info.host
            self.step.sql_request.user = source_info.user
            self.step.sql_request.password = decrypt_rsa_password(source_info.password)
            self.step.sql_request.port = source_info.port
        else:
            raise ValueError(f"{self.step.name} sql环境信息为空")
        return Step(RunSqlStep(self.step))

    async def __init_wait_step(self) -> Step:
        self.step.wait_request = TWaitRequest(**self.api_info.wait_request.dict())
        return Step(RunWaitStep(self.step))

    async def __init_if_step(self) -> Step:
        self.step.if_request = TIFRequest(**self.api_info.if_request.dict())
        self.step.if_request.check = parse_string_to_json(self.step.if_request.check)
        self.step.if_request.comparator = parse_string_to_json(self.step.if_request.comparator)
        self.step.if_request.expect = parse_string_to_json(self.step.if_request.expect)

        new_teststeps = []
        for step in self.api_info.if_request.teststeps:
            new_step_obj = (await HandleStepData().init(step)).step_obj
            new_teststeps.append(new_step_obj)
        self.step.if_request.teststeps = new_teststeps
        return Step(RunIFStep(self.step))

    async def __init_loop_step(self) -> Step:
        self.step.loop_request = TLoopRequest(**self.api_info.loop_request.dict())
        self.step.loop_request.for_variable_name = parse_string_to_json(self.step.loop_request.for_variable_name)
        self.step.loop_request.for_variable = parse_string_to_json(self.step.loop_request.for_variable)
        self.step.loop_request.while_comparator = parse_string_to_json(self.step.loop_request.while_comparator)
        self.step.loop_request.while_variable = parse_string_to_json(self.step.loop_request.while_variable)
        self.step.loop_request.while_value = parse_string_to_json(self.step.loop_request.while_value)
        new_teststeps = []
        for step in self.api_info.loop_request.teststeps:
            new_step_obj = (await HandleStepData().init(step)).step_obj
            new_teststeps.append(new_step_obj)
        self.step.loop_request.teststeps = new_teststeps
        return Step(RunLoopStep(self.step))

    async def __init_script_step(self) -> Step:
        self.step.script_request = TScriptRequest(**self.api_info.script_request.dict())
        return Step(RunScriptStep(self.step))

    async def init_request_headers(self):
        step_headers = handle_headers_or_validators(self.api_info.request.headers)
        self.step.request.headers = step_headers

    async def init_variables(self):
        """
        初始化变量
        """
        new_variables = handle_headers_or_validators(self.api_info.variables)
        self.step.variables.update(parse_validators_string_value(new_variables))

    async def init_setup_hooks(self):
        for step in self.api_info.setup_hooks:
            if step.enable is False:
                continue
            if isinstance(step, TStepData):
                step_info = await HandleStepData().init(ApiInfoIn(**step.dict()))
                self.step.setup_hooks.append(step_info.step_obj)

    async def init_teardown_hooks(self):
        for step in self.api_info.teardown_hooks:
            if step.enable is False:
                continue
            if isinstance(step, TStepData):
                step_info = await HandleStepData().init(ApiInfoIn(**step.dict()))
                self.step.teardown_hooks.append(step_info.step_obj)

    async def init_validators(self):
        if self.api_info.validators and isinstance(self.api_info.validators, typing.List):
            for vail in self.api_info.validators:
                # 解析字符串value
                vail.expect = parse_string_to_json(vail.expect)
                self.step.validators.append(vail.dict())


class HandelRunApiStep(object):
    config: typing.Union[TConfig, None]
    teststeps: typing.Union[typing.List[Step], None]
    api_info: typing.Union[ApiInfoIn, None]

    async def init(self, params: ApiInfoIn) -> "HandelRunApiStep":
        self.config = None
        self.teststeps: typing.List[Step] = []
        self.api_info = params
        await self.init_config()
        await self.init_steps(params)
        return self

    async def init_config(self):
        config_info = await HandleConfig().init(self.api_info.env_id, self.api_info.id)
        self.config = config_info.config
        self.config.name = self.api_info.name

    async def init_steps(self, steps: typing.Union[typing.List[TStepData], ApiInfoIn]):
        if isinstance(steps, ApiInfoIn):
            steps.case_id = steps.id
            step_info = await HandleStepData().init(steps)
            self.teststeps.append(step_info.step_obj)
        elif isinstance(steps, list):
            for step in steps:
                step_info = await HandleStepData().init(step)
                self.teststeps.append(step_info.step_obj)

    def get_testcase(self) -> "TestCase":
        return TestCase(config=self.config, teststeps=self.teststeps)


class HandelTestCase(object):
    config: typing.Union[TConfig, None]
    teststeps: typing.Union[typing.List[Step], None]
    api_case: typing.Union[TestCaseRun, None]

    async def init(self, params: TestCaseRun) -> "HandelTestCase":
        self.config = None
        self.teststeps = []
        self.api_case = params
        await self.init_config()
        await self.__init_headers()
        await self.__init_variables()
        await self.init_steps(params.step_data)
        return self

    async def init_config(self):
        config_info = await HandleConfig().init(self.api_case.env_id,
                                                self.api_case.id,
                                                self.api_case.headers,
                                                self.api_case.variables)
        self.config = config_info.config
        self.config.name = self.api_case.name
        self.config.step_rely = self.api_case.step_rely

    async def init_steps(self, steps: typing.List[TCaseStepData]) -> "HandelTestCase":
        step_data = await self.handle_steps(steps)
        for step in step_data:
            step_obj = (await HandleStepData().init(step)).step_obj
            self.teststeps.append(step_obj)
        return self

    @staticmethod
    async def handle_steps(steps: typing.List[TCaseStepData]) -> typing.List[TStepData]:
        new_step_data: typing.List[TStepData] = []
        for step in steps:
            if step.enable is False:
                continue
            new_step = None
            new_sub_steps = await HandelTestCase.handle_steps(step.sub_steps)
            if step.step_type.lower() == TStepTypeEnum.IF.value.lower():
                step.if_request.teststeps = new_sub_steps
                new_step = TStepData(**step.dict())
            elif step.step_type.lower() == TStepTypeEnum.loop.value.lower():
                step.loop_request.teststeps = new_sub_steps
                new_step = TStepData(**step.dict())
            elif step.step_type.lower() == TStepTypeEnum.api.value.lower():
                api_info = await ApiInfo.get(step.request.api_id, True)
                if api_info:
                    new_step = TStepData(**api_info)
                    new_step.case_id = api_info.get("id", None)
                else:
                    logger.error(f"没找到用例 {step.request.api_id}")
            else:
                new_step = TStepData(**step.dict())
            if new_step:
                new_step_data.append(new_step)
        return new_step_data

    def get_teststeps(self) -> typing.List[Step]:
        return self.teststeps

    async def __init_variables(self):
        if self.api_case.variables:
            new_validators = handle_headers_or_validators(self.api_case.variables)
            self.config.variables = parse_validators_string_value(new_validators)

    async def __init_headers(self):
        if self.api_case.headers:
            self.config.headers.update(handle_headers_or_validators(self.api_case.headers))

    def get_config(self) -> TConfig:
        return self.config

    def get_testcases(self) -> "TestCase":
        return TestCase(config=self.config, teststeps=self.teststeps)
