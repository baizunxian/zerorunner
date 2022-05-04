from loguru import logger

from autotest.corelibs.backend import celery
from autotest.httprunner.initialize_not_yaml import TestCaseMateNew
from autotest.services.api_services.test_case import CaseService


@celery.task()
def async_run_case(**kwargs):
    """异步执行用例"""
    CaseService.run(**kwargs)


@celery.task()
def run_timed_task(**kwargs):
    """定时任务运行"""
    base_url = kwargs.get('base_url', '')
    test_mate = TestCaseMateNew(base_url)
    run_type_data = CaseService.handle_run_type_batch(test_mate, **kwargs)
    test_path_set = test_mate.get_test_path_set()
    params = dict(test_path_set=test_path_set, run_type_data=run_type_data)
    logger.info('用例初始化完成~')
    CaseService.run(**params)
