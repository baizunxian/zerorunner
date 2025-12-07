# -*- coding: utf-8 -*-
# @author: 小白
import time
import typing

from loguru import logger

from zerorunner import exceptions
from zerorunner.database.db_utils import DBUtil
from zerorunner.models.base import TStepResultStatusEnum
from zerorunner.models.result_model import SqlResponseData, SessionData
from zerorunner.models.step_model import TStep, TSqlRequest
from zerorunner.parser import Parser
from zerorunner.response import ResponseObject, ResponseData
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep
from zerorunner.steps.step_result import TStepResult

from threading import Lock

from zerorunner.utils import default_serialize

lock = Lock()


def run_sql_request(runner: SessionRunner,
                    step: TStep,
                    step_tag: str = None,
                    parent_step_result: TStepResult = None):
    step_result = TStepResult(step, runner, step_tag=step_tag)
    step_result.start_log()
    start_time = time.time()
    step_result.result.session_data = SessionData()
    step_variables = runner.get_merge_variable(step)
    resp_obj = None
    try:
        request_dict = step.request.dict()

        # setup hooks
        if step.setup_hooks:
            step_result.set_step_log("前置hook开始~~~")
            runner.run_hooks(hooks=step.setup_hooks, hook_msg="setup_hooks", parent_step_result=step_result)
            step_result.set_step_log("前置hook结束~~~")

        # setup code
        if step.setup_code:
            try:
                step_result.set_step_log("前置code开始~~~")
                runner.run_script(script=step.setup_code,
                                  params=runner.config.script_modules,
                                  step=step)
                step_result.set_step_log(f"前置code结束  ~~~")
            except Exception as e:
                raise exceptions.MyBaseError(f"前置code执行失败: {e}")

        # 合并变量
        parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
        step.request = TSqlRequest(**parsed_request_dict)
        step_result.result.session_data.address.server_ip = step.request.host
        step_result.result.session_data.address.server_port = step.request.port
        step_result.result.session_data.request = TSqlRequest(**step.request.dict(exclude={'password'}))
        if not step.request.host and not step.request.port:
            raise exceptions.MyBaseError("host, port 请检查数据库信息，是否正确填写")
        db_engine = DBUtil(
            username=step.request.user,
            password=step.request.password,
            host=step.request.host,
            port=step.request.port,
            database=step.request.database
        )

        run_start_time = time.time()
        result = db_engine.execute_sql(step.request.sql)
        result = default_serialize(result)
        run_duration = round((time.time() - run_start_time) * 1000, 2)
        logger.info(f"SQL查询---> {step.request.sql}")
        resp_data = ResponseData(
            duration=run_duration,
            json_data=result
        )
        step_result.result.session_data.response = SqlResponseData(result=result)
        step_result.result.session_data.stat.response_time_ms = run_duration
        step_result.result.session_data.stat.content_size = len(str(result))

        resp_obj = ResponseObject(resp_data,
                                  step_type=step.step_type,
                                  parser=Parser(functions_mapping=runner.config.functions))
        # 提取
        with lock:
            extract_mapping = resp_obj.extract(step.extracts)
            runner.with_session_variables(extract_mapping)

            # teardown code
            if step.teardown_code:
                try:
                    step_result.set_step_log(f"后置code开始~~~")
                    runner.run_script(script=step.teardown_code,
                                      step=step,
                                      params=runner.config.script_modules)
                    step_result.set_step_log("后置code结束~~~")
                except Exception as e:
                    raise exceptions.MyBaseError(f"后置code执行失败: {e}")

            # teardown hooks
            if step.teardown_hooks:
                step_result.set_step_log("后置hook开始~~~")
                runner.run_hooks(hooks=step.teardown_hooks, hook_msg="teardown_hooks", parent_step_result=step_result)
                step_result.set_step_log("后置hook结束~~~")

            # 断言
            resp_obj.validate(step.validators, runner.get_merge_variable_pool())

        step_result.set_step_result_status(TStepResultStatusEnum.success)

    except exceptions.MyBaseFailure as err:
        step_result.set_step_result_status(TStepResultStatusEnum.fail)
        raise

    except (Exception, exceptions.MyBaseError) as err:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        raise
    except Exception as exc:
        step_result.set_step_result_status(TStepResultStatusEnum.err)
        step_result.result.session_data.success = False
        raise exc
    finally:
        step_result.end_log()
        step_result.result.session_data.success = step_result.result.success
        if resp_obj:
            step_result.result.session_data.validators = resp_obj.validation_results
            step_result.result.session_data.extracts = resp_obj.extract_results
        step_result = step_result.get_step_result()
        if parent_step_result:
            if parent_step_result:
                parent_step_result.set_step_log_not_show_time(step_result.log)
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result,
                                  step_tag=step_tag,
                                  parent_step_result=parent_step_result)


class RequestWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_host(self, host: str) -> "RequestWithOptionalArgs":
        self.__step.request.host = host
        return self

    def with_port(self, port: typing.Union[int, str]) -> "RequestWithOptionalArgs":
        self.__step.request.port = port
        return self

    def with_user(self, user: str) -> "RequestWithOptionalArgs":
        self.__step.request.user = user
        return self

    def with_password(self, password: str) -> "RequestWithOptionalArgs":
        self.__step.request.password = password
        return self

    def with_sql(self, sql: str) -> "RequestWithOptionalArgs":
        self.__step.request.sql = sql
        return self

    def with_timeout(self, timeout: str) -> "RequestWithOptionalArgs":
        self.__step.request.timeout = timeout
        return self

    def with_variable_name(self, variable_name: str) -> "RequestWithOptionalArgs":
        self.__step.request.variable_name = variable_name
        return self

    def teardown_hook(
            self, hook: str,
            assign_var_name: str = None
    ) -> "RequestWithOptionalArgs":
        if assign_var_name:
            self.__step.teardown_hooks.append({assign_var_name: hook})
        else:
            self.__step.teardown_hooks.append(hook)

        return self

    def struct(self) -> TStep:
        return self.__step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return f"request-{self.__step.request.method}"

    def run(self, runner: SessionRunner, **kwargs):
        return run_sql_request(runner, self.__step)


class RunSqlRequest(object):
    def __init__(self, name: str):
        self.__step = TStep(name=name)

    def with_step(self, step: TStep):
        self.__step = step
        return self

    def with_variables(self, **variables) -> "RunSqlRequest":
        self.__step.variables.update(variables)
        return self

    def with_retry(self, retry_times, retry_interval) -> "RunSqlRequest":
        self.__step.retry_times = retry_times
        self.__step.retry_interval = retry_interval
        return self

    def setup_hook(self, hook: str, assign_var_name: str = None) -> "RunSqlRequest":
        if assign_var_name:
            self.__step.setup_hooks.append({assign_var_name: hook})
        else:
            self.__step.setup_hooks.append(hook)

        return self


class RunSqlStep(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def name(self) -> str:
        return self.__step.name

    def type(self) -> str:
        return self.__step.step_type

    def struct(self) -> TStep:
        return self.__step

    def run(self, runner: SessionRunner, **kwargs):
        return run_sql_request(runner, self.__step, **kwargs)
