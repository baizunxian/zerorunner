# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import time
import typing
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock

from loguru import logger

from autotest.init.redis_init import MyAsyncRedis
from autotest.models.api_models import ApiCase, ApiTestReport
from autotest.schemas.api.api_case import TestCaseRun
from autotest.schemas.api.api_info import ApiRunSchema
from autotest.schemas.api.api_report import TestReportSaveSchema
from autotest.services.api import api_info
from autotest.services.api.api_case import ApiCaseService
from autotest.services.api.api_report import ReportService
from autotest.services.api.run_handle_new import HandelTestCase
from autotest.utils.consts import TEST_EXECUTE_SET, TEST_EXECUTE_STATS, CACHE_WEEK, TEST_EXECUTE_TASK
from autotest.utils.local import g
from celery_worker.worker import celery
from config import config
from zerorunner.models.step_model import TestCase
from zerorunner.testcase import ZeroRunner

executor_worker = ThreadPoolExecutor(max_workers=4)

r_lock = Lock()
t_lock = Lock()


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
    r: MyAsyncRedis = g.redis
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
        summary = runner.run_tests(testcase)
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
        # 用例列表
        testcase_list_key = TEST_EXECUTE_SET.format(report_id)
        # 运行统计
        testcase_static_key = TEST_EXECUTE_STATS.format(report_id)
        testcase_task_key = TEST_EXECUTE_TASK.format(report_id)
        # testcase_queue = Queue()
        for step in testcase.teststeps:
            new_testcase = TestCase(config=testcase.config, teststeps=[step])
            await r.cus_lpush_by_pickle(testcase_list_key, new_testcase.dict(by_alias=True))
            # testcase_queue.put(new_testcase)

        # 设置默认统计数据
        await r.set(testcase_static_key, report_params.dict(), CACHE_WEEK)
        # 设置运行任务
        await r.set(testcase_task_key, config.task_run_pool)
        # 设置ttl 7天
        await r.expire(testcase_list_key, CACHE_WEEK)

        # with ThreadPoolExecutor(max_workers=config.task_run_pool) as executor:
        #     task = executor.submit(lambda q: run_step_by_queue(*q), (testcase_queue, report_id, r))
        #     for i in as_completed([task]):
        #         a = i.result()
        #         print(a)

        [run_case_step.delay(report_id) for _ in range(config.task_run_pool)]


@celery.task
async def run_case_step(report_id: typing.Union[str, int], callback: typing.Callable = None):
    """运行用例步骤"""
    r: MyAsyncRedis = g.redis
    testcase_list_key = TEST_EXECUTE_SET.format(report_id)
    testcase_static_key = TEST_EXECUTE_STATS.format(report_id)
    testcase_task_key = TEST_EXECUTE_TASK.format(report_id)
    try:
        report_info = await ApiTestReport.get(report_id, to_dict=True)
        exec_user_id = report_info.get("exec_user_id", None)
        exec_user_name = report_info.get("exec_user_name", None)
        while await r.llen(testcase_list_key):
            testcase_dict = await r.cus_lpop_by_pickle(testcase_list_key)
            if testcase_dict:
                testcase = TestCase.parse_obj(testcase_dict)
                runner = ZeroRunner()
                summary = runner.run_tests(testcase)

                if r_lock.acquire():
                    static_dict = await r.get(testcase_static_key)
                    static_dict["run_count"] = static_dict["run_count"] + summary.run_count
                    static_dict["run_success_count"] = static_dict["run_success_count"] + summary.run_success_count
                    static_dict["run_skip_count"] = static_dict["run_skip_count"] + summary.run_skip_count
                    static_dict["run_fail_count"] = static_dict["run_fail_count"] + summary.run_fail_count
                    static_dict["run_err_count"] = static_dict["run_err_count"] + summary.run_err_count
                    static_dict["actual_run_count"] = static_dict["actual_run_count"] + summary.actual_run_count
                    static_dict["duration"] = static_dict["duration"] + summary.duration
                    await r.set(testcase_static_key, static_dict)
                    r_lock.release()

                await ReportService.save_report_detail(summary=summary,
                                                       report_id=report_id,
                                                       exec_user_id=exec_user_id,
                                                       exec_user_name=exec_user_name)

    except Exception as exc:

        logger.error(f"用例执行错误，报告id: {report_id} 错误信\n{exc}")
    finally:
        if t_lock.acquire():
            await r.decrby(testcase_task_key)
            t_lock.release()

        run_test_num = await r.get(testcase_task_key)
        if run_test_num == 0:
            report_info = await ApiTestReport.get(report_id, to_dict=True)
            static_dict = await r.get(testcase_static_key)
            report_info.update(static_dict)
            summary_params = TestReportSaveSchema.parse_obj(report_info)
            summary_params.success = static_dict["run_err_count"] == 0 and static_dict["run_fail_count"] == 0
            await ReportService.save_report_info(summary_params)
            await r.delete(testcase_static_key)
            await r.delete(testcase_task_key)

        if callback:
            callback()


def run_step_by_queue(testcase_queue: Queue, report_id: typing.Union[str, int], my_redis):
    """通过队列运行步骤"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r: MyRedis = my_redis

    task = loop.create_task(ApiTestReport.get(report_id, True))
    report_info = loop.run_until_complete(task)
    exec_user_id = report_info.get("exec_user_id", None)
    exec_user_name = report_info.get("exec_user_name", None)
    while not testcase_queue.empty():
        testcase: TestCase = testcase_queue.get()
        testcase_static_key = TEST_EXECUTE_STATS.format(report_id)
        runner = ZeroRunner()
        summary = runner.run_tests(testcase)

        static_dict = r.get(testcase_static_key)
        if r_lock.acquire():
            static_dict["run_count"] = static_dict["run_count"] + summary.run_count
            static_dict["run_success_count"] = static_dict["run_success_count"] + summary.run_success_count
            static_dict["run_skip_count"] = static_dict["run_skip_count"] + summary.run_skip_count
            static_dict["run_fail_count"] = static_dict["run_fail_count"] + summary.run_fail_count
            static_dict["run_err_count"] = static_dict["run_err_count"] + summary.run_err_count
            static_dict["actual_run_count"] = static_dict["actual_run_count"] + summary.actual_run_count
            static_dict["duration"] = static_dict["duration"] + summary.duration
            r.set(testcase_static_key, static_dict)
            r_lock.release()

        ReportService.save_report_detail(summary=summary,
                                         report_id=report_id,
                                         exec_user_id=exec_user_id,
                                         exec_user_name=exec_user_name)
    logger.info('完成---1')


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
