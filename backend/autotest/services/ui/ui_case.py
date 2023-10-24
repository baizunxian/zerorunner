# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.exceptions.exceptions import ParameterError
from autotest.models.ui_models import UiCase
from autotest.schemas.api.api_case import TestCaseRun, TCaseStepData
from autotest.schemas.step_data import TStepData
from autotest.schemas.ui.ui_case import UiCaseQuery, UiCaseId, UiCaseIn
from autotest.services.api.run_handle_new import HandelTestCase
from autotest.services.ui.ui_report import UiReportService
from autotest.utils.current_user import current_user
from zerorunner.ext.zero_driver.driver import ZeroDriver, DriverSetting
from zerorunner.models.step_model import TUiRequest
from zerorunner.runner import SessionRunner
from zerorunner.testcase import ZeroRunner


class UiCaseServer:
    """ui用例服务"""

    @staticmethod
    async def list(params: UiCaseQuery):
        """获取用例列表"""
        return await UiCase.get_list(params)

    @staticmethod
    async def get_case_by_id(params: UiCaseId):
        """根据id获取用例信息"""
        if not params.id:
            raise ParameterError("id不能为空")
        page_info = await UiCase.get_case_by_id(params.id)
        if not page_info:
            raise ParameterError("UI页面信息不存在")
        return page_info

    @staticmethod
    async def save_or_update(params: UiCaseIn):
        """保存或更新用例信息"""
        page_info = await UiCase.create_or_update(params.dict())
        return await UiCaseServer.get_case_by_id(UiCaseId(id=page_info['id']))

    @staticmethod
    async def deleted(id: int):
        """删除用例信息"""
        return await UiCase.delete(id)

    @staticmethod
    async def run_ui_case_by_id(params: UiCaseId):
        """根据id运行用例信息"""
        ui_case_info = await UiCaseServer.get_case_by_id(params)
        if not ui_case_info:
            raise ParameterError("UI用例信息不存在")
        ui_case_info = UiCaseIn.parse_obj(ui_case_info)

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

        current_user_info = await current_user()
        summary_params = await UiReportService.get_report_result(summary,
                                                                 ui_case_info.api_case.project_id,
                                                                 ui_case_info.api_case.module_id,
                                                                 ui_case_info.api_case.env_id,
                                                                 ex_user_id=current_user_info.get("id", None))
        ui_report_info = await UiReportService.save_report_info(summary_params)
        ui_report_id = ui_report_info.get("id")
        await UiReportService.save_report_detail(summary, ui_report_id)

        return summary

    @staticmethod
    async def debug_ui_case(params: UiCaseIn):
        api_case_info = await UiCaseServer.handel_ui_case2run_schemas(params)
        session_runner = SessionRunner()
        driver_setting = DriverSetting(
            command_executor="http://xiaobaicodes.com:4444/wd/hub",
            headless=False
        )
        zero_driver = ZeroDriver(driver_setting)
        session_runner.zero_driver = zero_driver
        runner = ZeroRunner(session_runner=session_runner)
        testcase = api_case_info.get_testcases()
        summary = runner.run_tests(testcase)
        return summary

    @staticmethod
    async def handel_ui_case2run_schemas(ui_case: UiCaseIn):
        """处理用例信息"""
        step_data = []
        if ui_case.steps:
            for step in ui_case.steps:
                case_step = TStepData(
                    case_id=ui_case.id,
                    name=step.name,
                    index=step.index,
                    step_type='ui',
                    enable=step.enable,
                    variables=step.variables,
                    request=TUiRequest(
                        action=step.action,
                        data=step.data,
                        location_value=step.location_value,
                        location_method=step.location_method,
                        cookie=step.cookie,
                        output=step.output,
                    ),
                )
                step_data.append(case_step)
        run_params = TestCaseRun(id=ui_case.id,
                                 name=ui_case.name,
                                 env_id=None,
                                 project_id=ui_case.project_id,
                                 module_id=ui_case.module_id,
                                 remarks=ui_case.remarks,
                                 variables=ui_case.variables,
                                 step_data=step_data)
        api_case_info = await HandelTestCase().init(run_params)
        return api_case_info

    @staticmethod
    async def get_count_by_user():
        """获取用户api数量"""
        user_info = await current_user()
        count_info = await UiCase.get_count_by_user_id(user_info.get("id", None))
        if not count_info:
            return 0
        if count_info:
            return count_info.get("count", 0)
