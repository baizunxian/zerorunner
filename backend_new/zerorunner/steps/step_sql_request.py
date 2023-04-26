# -*- coding: utf-8 -*-
# @author: xiaobai
import time
import traceback
import typing

from loguru import logger
from zerorunner.database.engine import DBEngine
from zerorunner.model.step_model import TStep, TSqlRequest
from zerorunner.models import TStepLogType, StepResult, TStepResultStatusEnum
from zerorunner.runner import SessionRunner
from zerorunner.steps.base import IStep


def run_sql_request(runner: SessionRunner,
                    step: TStep,
                    step_tag: str = None,
                    parent_step_result: StepResult = None):
    step_result = runner.get_step_result(step, step_tag)
    runner.set_run_log(step_result=step_result, log_type=TStepLogType.start)
    start_time = time.time()
    step_variables = runner.get_merge_variable(step)
    request_dict = step.sql_request.dict()
    parsed_request_dict = runner.parser.parse_data(request_dict, step_variables)
    step.sql_request = TSqlRequest(**parsed_request_dict)
    try:
        db_engine = DBEngine(
            f'mysql+pymysql://{step.sql_request.user}:'
            f'{step.sql_request.password}@{step.sql_request.host}:'
            f'{step.sql_request.port}/{step.sql_request.database}'
            f"?charset=utf8mb4"
        )

        data = db_engine.fetchall(step.sql_request.sql)
        variables = {step.sql_request.variable_name: data}
        runner.with_variables(variables)
        step_result.export_vars.update(variables)
        logger.info(f"SQL查询---> {step.sql_request.sql}")
        runner.set_run_log(f"SQL查询-> 设置变量:{step.sql_request.variable_name}, 设置变量值：{data}")
        runner.set_step_result_status(step_result, TStepResultStatusEnum.success)
        runner.with_session_variables(variables)
    except Exception as err:
        runner.set_step_result_status(step_result, TStepResultStatusEnum.err, str(err))
        raise
    finally:
        step_result.duration = time.time() - start_time
        runner.append_step_result(step_result=step_result, step_tag=step_tag, parent_step_result=parent_step_result)
        runner.set_run_log(step_result=step_result, log_type=TStepLogType.end)


class RequestWithOptionalArgs(IStep):
    def __init__(self, step: TStep):
        self.__step = step

    def with_host(self, host: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.host = host
        return self

    def with_port(self, port: typing.Union[int, str]) -> "RequestWithOptionalArgs":
        self.__step.sql_request.port = port
        return self

    def with_user(self, user: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.user = user
        return self

    def with_password(self, password: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.password = password
        return self

    def with_sql(self, sql: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.sql = sql
        return self

    def with_timeout(self, timeout: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.timeout = timeout
        return self

    def with_variable_name(self, variable_name: str) -> "RequestWithOptionalArgs":
        self.__step.sql_request.variable_name = variable_name
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
