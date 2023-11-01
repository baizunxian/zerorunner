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
from autotest.schemas.api.api_case import TestCaseRun
from autotest.schemas.api.api_info import ApiInfoIn
from autotest.schemas.step_data import TStepData, RequestMode, ApiBaseSchema, RawLanguageEnum, TRequestData, TSqlData
from autotest.utils.des import decrypt_rsa_password
from config import config
from zerorunner.loader import load_module_functions, load_func_content
from zerorunner.models.base import TStepTypeEnum
from zerorunner.models.step_model import TStep, TRequest, TSqlRequest, TIFRequest, TLoopRequest, TScriptRequest, \
    TWaitRequest, TestCase, TUiRequest, TConfig
from zerorunner.parser import Parser
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


def handle_headers_or_validators(param: typing.List[ApiBaseSchema], type: str = None) -> typing.Dict:
    """处理请求头，跟变量
    args  param List[ApiCaseBaseSchema] 对象
    [
        {
        "key": "test",
        "value": "test_value",
        "remarks": "测试",
        }
    ]
    type 类型 如有是请求头则吧不是字符串的value转成字符串

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
            p = ApiBaseSchema.parse_obj(p)
        if type == "headers" and not isinstance(p.value, str):
            p.value = str(p.value)
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
        env_headers = {}
        env_variables = {}
        if env_info:
            # 环境初始化
            # 环境域名
            if env_info.domain_name:
                self.config.base_url = env_info.domain_name

            # 环境变量
            if env_info.variables:
                new_variables = handle_headers_or_validators(env_info.variables)
                # 43 修复环境变量覆盖用例变量
                env_variables.update(parse_validators_string_value(new_variables))
            # 环境请求头
            if env_info.headers:
                env_headers.update(handle_headers_or_validators(env_info.headers, type="headers"))
        config_funcs = await EnvFunc.get_by_env_id(env_id) if env_id else []
        if config_funcs:
            for func in config_funcs:
                func_content = func.get("content", None)
                if func_content:
                    self.config.functions.update(
                        load_func_content(func_content, f"{func.get('name', '')}{uuid.uuid4().hex}"))
        try:
            env_headers = Parser(self.config.functions).parse_data(env_headers, env_variables)
            self.config.headers.update(env_headers)
            env_variables = Parser(self.config.functions).parse_data(env_variables, env_variables)
            self.config.env_variables.update(env_variables)
        except Exception as exc:
            logger.error(f"环境配置初始化失败 env_id:{env_id}: {exc}")
            raise ValueError(f"环境配置初始化失败 env_id:{env_id}: {exc}")

    async def init_headers(self, headers: typing.List[ApiBaseSchema]):
        self.config.headers.update(handle_headers_or_validators(headers, type="headers"))

    async def init_variables(self, variables: typing.List[ApiBaseSchema]):
        new_variables = handle_headers_or_validators(variables)
        self.config.variables.update(parse_validators_string_value(new_variables))

    async def init_functions(self):
        from autotest.utils import basic_function
        self.config.functions.update(load_module_functions(basic_function))


class HandleStepData(object):
    api_info: TStepData
    config: TConfig
    step: TStep = None
    step_obj: typing.Union[Step, None] = None

    # 排除需要处理的参数

    async def init(self, params: TStepData, case_id: typing.Union[str, int] = None) -> "HandleStepData":
        # 过滤需要处理的数据 其他参数一次性赋值给TStep对象
        exclude_set = {"case_id", "request", "variables", "setup_hooks", "teardown_hooks", "validators",
                       "children_steps"}
        self.case_id = case_id
        self.step = TStep(**params.dict(exclude=exclude_set), case_id=case_id)
        self.api_info = params
        self.step_obj = None
        await self.init_step()
        return self

    async def init_step(self):
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
        else:
            raise ValueError(f"步骤类型错误：{step_type}")

        await self.init_variables()
        await self.init_setup_hooks()
        await self.init_teardown_hooks()
        await self.init_validators()
        self.step_obj = step_obj

    async def __init_api_step(self) -> Step:
        self.step.request = TRequest(method=self.api_info.request.method, url=self.api_info.request.url)
        request_mode = self.api_info.request.mode.lower()
        if request_mode == RequestMode.RAW.value.lower():
            # json
            if self.api_info.request.language.lower() == RawLanguageEnum.JSON.value:
                try:
                    self.step.request.req_json = json.loads(self.api_info.request.data)
                except Exception:
                    logger.error(traceback.format_exc())
                    self.step.request.data = self.api_info.request.data
            # # text
            # elif self.api_info.request.language.lower() == RawLanguageEnum.TEXT.value:
            #     self.step.request.data = self.api_info.request.data
            else:
                self.step.request.data = self.api_info.request.data
        elif request_mode == RequestMode.FORM_DATA.value:
            upload_dict = {}
            for data in self.api_info.request.data or []:
                if data.type == RequestMode.FILE.value:
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
        elif request_mode == RequestMode.X_WWW_FORM_URLENCODED.value:
            form_urlencoded_dict = {}
            for data in self.api_info.request.data or []:
                form_urlencoded_dict[data.key] = data.value
            self.step.request.data = form_urlencoded_dict

        elif request_mode == RequestMode.none.value.lower():
            self.step.request.data = None
        return Step(RunRequestStep(self.step))

    async def __init_ui_step(self) -> Step:
        self.step.request = TUiRequest.parse_obj(self.api_info.request.dict())
        return Step(RunUiStep(self.step))

    async def __init_sql_step(self) -> Step:
        """sql步骤初始化"""
        source_info = await DataSource.get(self.api_info.request.source_id)
        self.step.request = TSqlRequest.parse_obj(self.api_info.request)
        if source_info:
            self.step.request.host = source_info.host
            self.step.request.user = source_info.user
            self.step.request.password = decrypt_rsa_password(source_info.password)
            self.step.request.port = source_info.port
        else:
            raise ValueError(f"{self.step.name} sql环境信息为空")
        return Step(RunSqlStep(self.step))

    async def __init_wait_step(self) -> Step:
        """wait步骤初始化"""
        self.step.request = TWaitRequest.parse_obj(self.api_info.request)
        return Step(RunWaitStep(self.step))

    async def __init_if_step(self) -> Step:
        """if步骤初始化"""
        self.step.request = TIFRequest.parse_obj(self.api_info.request.dict())
        self.step.request.check = parse_string_to_json(self.step.request.check)
        self.step.request.comparator = parse_string_to_json(self.step.request.comparator)
        self.step.request.expect = parse_string_to_json(self.step.request.expect)

        new_children_steps = []
        for c_step in self.api_info.children_steps:
            new_step_obj = (await HandleStepData().init(c_step, case_id=self.case_id)).step_obj
            new_children_steps.append(new_step_obj)
        self.step.children_steps = new_children_steps

        return Step(RunIFStep(self.step))

    async def __init_loop_step(self) -> Step:
        """loop步骤初始化"""
        self.step.request = TLoopRequest.parse_obj(self.api_info.request.dict())
        self.step.request.for_variable_name = parse_string_to_json(self.step.request.for_variable_name)
        self.step.request.for_variable = parse_string_to_json(self.step.request.for_variable)
        self.step.request.while_comparator = parse_string_to_json(self.step.request.while_comparator)
        self.step.request.while_variable = parse_string_to_json(self.step.request.while_variable)
        self.step.request.while_value = parse_string_to_json(self.step.request.while_value)

        new_children_steps = []
        for c_step in self.api_info.children_steps:
            new_step_obj = (await HandleStepData().init(c_step, self.case_id)).step_obj
            new_children_steps.append(new_step_obj)
        self.step.children_steps = new_children_steps

        return Step(RunLoopStep(self.step))

    async def __init_script_step(self) -> Step:
        """script步骤初始化"""
        self.step.request = TScriptRequest.parse_obj(self.api_info.request)
        return Step(RunScriptStep(self.step))

    async def init_request_headers(self):
        """初始化请求头"""
        step_headers = handle_headers_or_validators(self.api_info.request.headers, type="headers")
        self.step.request.headers = step_headers

    async def init_variables(self):
        """初始化变量"""
        new_variables = handle_headers_or_validators(self.api_info.variables)
        self.step.variables.update(parse_validators_string_value(new_variables))

    async def init_setup_hooks(self):
        """初始化前置钩子"""
        for step in self.api_info.setup_hooks:
            if step.enable is False:
                continue
            if isinstance(step, TStepData):
                step_info = await HandleStepData().init(ApiInfoIn.parse_obj(step.dict()), self.case_id)
                self.step.setup_hooks.append(step_info.step_obj)

    async def init_teardown_hooks(self):
        """初始化后置钩子"""
        for step in self.api_info.teardown_hooks:
            if step.enable is False:
                continue
            if isinstance(step, TStepData):
                step_info = await HandleStepData().init(ApiInfoIn.parse_obj(step.dict()), self.case_id)
                self.step.teardown_hooks.append(step_info.step_obj)

    async def init_validators(self):
        """初始化断言"""
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
            step_info.step.source_id = steps.id
            self.teststeps.append(step_info.step_obj)
        elif isinstance(steps, list):
            for step in steps:
                step_info = await HandleStepData().init(step)
                step_info.step.source_id = step.id
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

    async def init_steps(self, steps: typing.List[TStepData]) -> "HandelTestCase":
        step_data = await self.handle_steps(steps)
        for step in step_data:
            step_obj = (await HandleStepData().init(step, self.api_case.id)).step_obj
            self.teststeps.append(step_obj)
        return self

    @staticmethod
    async def handle_steps(steps: typing.List[typing.Union[TStepData]]) -> typing.List[TStepData]:
        new_step_data: typing.List[TStepData] = []
        for step in steps:
            if step.enable is False:
                continue
            new_step = None
            step.children_steps = await HandelTestCase.handle_steps(step.children_steps)
            if step.step_type.lower() == TStepTypeEnum.api.value.lower():
                # 处理api用例，后面会支持是否是引用模式
                api_info = await ApiInfo.get(step.source_id, True)
                if api_info:
                    if step.is_quotation:
                        new_step = TStepData.parse_obj(api_info)
                    else:
                        new_step = TStepData.parse_obj(step.dict())
                    new_step.source_id = api_info.get("id", None)
                    new_step.index = step.index
                else:
                    logger.error(f"没找到用例 {step.source_id}")
            else:
                new_step = TStepData.parse_obj(step.dict())
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
