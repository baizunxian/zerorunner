# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import time
import typing
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from loguru import logger
from pydantic import BaseModel

from autotest.db.session import sync_session, SQLAlchemySession
from autotest.models.api_models import ApiCase, ApiTestReport
from autotest.schemas.api.api_case import TestCaseRun
from autotest.schemas.api.api_info import ApiRunSchema
from autotest.schemas.api.api_report import TestReportSaveSchema
from autotest.services.api import api_info
from autotest.services.api.api_case import ApiCaseService
from autotest.services.api.api_report import ReportService
from autotest.services.api.run_handle_new import HandelTestCase
from autotest.utils.sync import sync_to_async
from celery_worker.worker import celery
from zerorunner.models.step_model import TestCase
from zerorunner.testcase import ZeroRunner

executor_worker = ThreadPoolExecutor(max_workers=4)

r_lock = Lock()
t_lock = Lock()


class TestCaseRunStatistics(BaseModel):
    """用例运行统计"""
    run_count: int = 0
    run_success_count: int = 0
    run_skip_count: int = 0
    run_fail_count: int = 0
    run_err_count: int = 0
    actual_run_count: int = 0
    duration: float = 0


@celery.task
async def async_run_api(**kwargs: typing.Any):
    """
    异步执行接口
    :param kwargs: 执行参数
    :return:
    """
    params = ApiRunSchema(**kwargs)
    logger.info("start run api")
    await api_info.ApiInfoService.run(params)


@celery.task
async def async_run_testcase(case_id: typing.Union[str, int], report_id: [str, int] = None, **kwargs: typing.Any):
    """
    运行测试用例
    :param case_id: 用例id
    :param report_id: 报告id默认None
    :param kwargs: 其他参数
    :return:
    """
    exec_user_id = kwargs.get("exec_user_id", None)
    exec_user_name = kwargs.get("exec_user_name", None)
    run_mode = kwargs.get("run_mode", 20)
    run_type = kwargs.get("run_type", "case")
    if not case_id:
        raise ValueError("id 不能为空！")
    case_info = await ApiCase.get(case_id, to_dict=True)
    if not case_id:
        logger.error(f"用例id: {case_id} 不存在！")
        return
    await ApiCaseService.set_step_data(case_info)
    run_params: TestCaseRun = TestCaseRun(**case_info, env_id=kwargs.get('case_env_id', None))
    if not report_id:
        """没有报告id创建报告"""
        report_params = TestReportSaveSchema(
            name=case_info["name"],
            case_id=case_info["id"],
            run_mode=run_mode,
            run_type=run_type,
            project_id=case_info["project_id"],
            module_id=run_params.module_id,
            env_id=run_params.env_id,
            exec_user_id=exec_user_id,
            exec_user_name=exec_user_name,
            start_time=time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time()))
        )
        report_info = await ReportService.save_report_info(report_params)
        report_id = report_info.get("id")
        report_params = TestReportSaveSchema.parse_obj(report_info)
    else:

        report_info = await ApiTestReport.get(report_id, to_dict=True)
        report_params = TestReportSaveSchema.parse_obj(report_info)

    # 初始化用例
    try:
        api_case_info = await HandelTestCase().init(run_params)
    except Exception as exc:
        logger.error(f"用例初始化失败！用例id: {case_id} 错误信息：{exc}")
        report_params.error_msg = f"用例初始化失败！用例id: {case_id} 错误信息：{exc}"
        await ReportService.save_report_info(report_params)
        raise RuntimeError(f"用例初始化失败！用例id: {case_id} 错误信息：\n{exc}")

    if run_params.step_rely:  # 步骤依赖:
        runner = ZeroRunner()
        # await api_case_info.init_config()
        testcase = api_case_info.get_testcases()
        summary = await sync_to_async(runner.run_tests)(testcase)
        logger.info(f"执行成功！--- report_id: {report_id}")
        report_params.run_count = summary.run_count
        report_params.run_success_count = summary.run_success_count
        report_params.run_skip_count = summary.run_skip_count
        report_params.run_fail_count = summary.run_fail_count
        report_params.run_err_count = summary.run_err_count
        report_params.duration = summary.duration
        report_params.start_time = summary.start_time
        report_params.actual_run_count = summary.actual_run_count
        summary_params = TestReportSaveSchema.parse_obj(report_params.dict())
        summary_params.success = summary.success
        await ReportService.save_report_info(summary_params)
        await ReportService.save_report_detail(summary,
                                               report_id,
                                               case_name=case_info.get("name", None),
                                               exec_user_id=exec_user_id,
                                               exec_user_name=exec_user_name)
    else:
        report_params.duration = report_params.duration if report_params.duration else 0
        testcase = api_case_info.get_testcases()

        case_queue = asyncio.Queue()
        for step in testcase.teststeps:
            new_testcase = TestCase(config=testcase.config, teststeps=[step])
            await case_queue.put(new_testcase)

        start_time = time.time()
        session = sync_session
        result = await asyncio.gather(*(run_case_step(report_id, case_queue, session,
                                                      exec_user_id=report_params.exec_user_id,
                                                      exec_user_name=report_params.exec_user_name) for _ in
                                        range(10)))
        logger.debug(f"执行耗时！--- report_id: {report_id} 耗时：{time.time() - start_time}")
        duration = time.time() - start_time
        case_run_statistics = TestCaseRunStatistics()
        for res in result:
            case_run_statistics.run_count += res.run_count
            case_run_statistics.run_success_count += res.run_success_count
            case_run_statistics.run_skip_count += res.run_skip_count
            case_run_statistics.run_fail_count += res.run_fail_count
            case_run_statistics.run_err_count += res.run_err_count
            case_run_statistics.actual_run_count += res.actual_run_count
            # case_run_statistics.duration += res.duration
        case_run_statistics.duration = duration
        report_info = await ApiTestReport.get(report_id, to_dict=True)
        report_info.update(case_run_statistics.dict())
        summary_params = TestReportSaveSchema(**report_info)
        summary_params.success = case_run_statistics.run_err_count == 0 and case_run_statistics.run_fail_count == 0
        await ReportService.save_report_info(summary_params)


async def run_case_step(report_id: typing.Union[str, int], case_queue: asyncio.Queue, session,
                        **kwargs) -> TestCaseRunStatistics:
    """运行用例步骤"""
    exec_user_id = kwargs.get("exec_user_id", None)
    exec_user_name = kwargs.get("exec_user_name", None)
    test_run_statistics = TestCaseRunStatistics()
    try:
        while not case_queue.empty():
            testcase = await case_queue.get()
            runner = ZeroRunner()
            summary = await sync_to_async(runner.run_tests)(testcase)
            test_run_statistics.run_count += summary.run_count
            test_run_statistics.run_success_count += summary.run_success_count
            test_run_statistics.run_skip_count += summary.run_skip_count
            test_run_statistics.run_fail_count += summary.run_fail_count
            test_run_statistics.run_err_count += summary.run_err_count
            test_run_statistics.duration += summary.duration
            test_run_statistics.actual_run_count += summary.actual_run_count

            async with session() as connect:
                SQLAlchemySession.set(connect)
                await ReportService.save_report_detail(summary=summary,
                                                       report_id=report_id,
                                                       exec_user_id=exec_user_id,
                                                       exec_user_name=exec_user_name)
    except Exception as exc:
        logger.error(f"用例执行错误，报告id: {report_id} 错误信\n{exc}")

    return test_run_statistics

