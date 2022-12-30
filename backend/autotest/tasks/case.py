from loguru import logger

from autotest.corelibs.backend import celery
from autotest.httprunner.initialize_not_yaml import TestCaseMateNew
from autotest.models.api_models import ApiInfo, ApiCase
from autotest.services.api_services.api_info import ApiInfoService
from autotest.services.api_services.run_handle import ApiInfoHandle, ApiCaseHandle
from autotest.services.api_services.test_report import ReportService
from autotest.tasks.models import AsyncRunCaseSchema
from autotest.utils.api import jsonable_encoder
from zerorunner.runner import Runner


@celery.task()
def async_run_case(**kwargs):
    """异步执行用例"""
    params = AsyncRunCaseSchema(**kwargs)
    zr = Runner()
    case_info = None

    project_id = None
    module_id = None
    env_id = None

    if params.run_mode == "case":
        case_info = ApiInfo.get(params.id)
        case_info = ApiInfoHandle(**jsonable_encoder(case_info))
        zr.teststeps = [case_info.step]
        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id

    elif params.run_mode == "suites":
        case_info = ApiCase.get(params.id)
        case_info = ApiCaseHandle(**jsonable_encoder(case_info))
        zr.teststeps = case_info.teststeps
        project_id = case_info.api_suites.project_id
        module_id = case_info.api_suites.module_id
        env_id = case_info.api_suites.env_id
    if case_info:
        zr.config = case_info.config
        zr.run()
        summary = zr.get_summary()
        ReportService.save_report(summary, project_id, module_id, env_id)


@celery.task()
def run_timed_task(**kwargs):
    """定时任务运行"""
    base_url = kwargs.get('base_url', '')
    test_mate = TestCaseMateNew(base_url)
    run_type_data = ApiInfoService.handle_run_type_batch(test_mate, **kwargs)
    test_path_set = test_mate.get_test_path_set()
    params = dict(test_path_set=test_path_set, run_type_data=run_type_data)
    logger.info('用例初始化完成~')
    ApiInfoService.run(**params)
