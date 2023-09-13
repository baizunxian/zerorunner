# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from threading import Lock

from loguru import logger

from autotest.models.ui_models import UiCase
from autotest.schemas.ui.ui_case import UiCaseIn
from autotest.services.ui.ui_case import UiCaseServer
from autotest.services.ui.ui_report import UiReportService
from celery_worker.worker import celery
from zerorunner.ext.zero_driver.driver import DriverSetting, ZeroDriver
from zerorunner.runner import SessionRunner
from zerorunner.testcase import ZeroRunner

r_lock = Lock()
t_lock = Lock()


@celery.task
async def async_run_ui(ui_id: typing.Union[str, int], report_id: [str, int] = None, **kwargs: typing.Any):
    """
    运行测试用例
    :param ui_id: 用例id
    :param report_id: 报告id默认None
    :param kwargs: 其他参数
    :return:
    """
    exec_user_id = kwargs.get("exec_user_id", None)
    exec_user_name = kwargs.get("exec_user_name", None)
    if not ui_id:
        raise ValueError("ui id 不能为空！")
    ui_case_info = await UiCase.get(ui_id, to_dict=True)
    if not ui_case_info:
        logger.error(f"ui 用例id: {ui_id} 不存在！")
        return

    env_id = kwargs.get("ui_env_id", None)

    ui_case_info = UiCaseIn(**ui_case_info)

    ui_case_info = await UiCaseServer.handel_ui_case2run_schemas(ui_case_info)
    session_runner = SessionRunner()
    driver_setting = DriverSetting(
        command_executor="http://xiaobaicodes.com:4444/wd/hub",
        headless=False
    )
    zero_driver = ZeroDriver(driver_setting)
    session_runner.zero_driver = zero_driver
    runner = ZeroRunner(session_runner=session_runner)
    testcase = ui_case_info.get_testcases()
    summary = runner.run_tests(testcase)
    zero_driver.quit()

    summary_params = await UiReportService.get_report_result(summary,
                                                             project_id=ui_case_info.api_case.project_id,
                                                             module_id=ui_case_info.api_case.module_id,
                                                             env_id=env_id,
                                                             exec_user_id=exec_user_id,
                                                             exec_user_name=exec_user_name)
    ui_report_info = await UiReportService.save_report_info(summary_params)
    ui_report_id = ui_report_info.get("id")
    await UiReportService.save_report_detail(summary, ui_report_id)
