import time
import traceback
import typing

from loguru import logger

from autotest.models.ui_models import UiReports, UiReportDetail
from autotest.schemas.ui.ui_report import UiReportSaveSchema, UiReportQuery, UiReportId, UiReportDetailQuery
from autotest.services.system.file import FileService
from autotest.utils.common import get_time
from zerorunner.models.result_model import TestCaseSummary, StepResult


class UiReportService:

    @staticmethod
    async def list(params: UiReportQuery) -> typing.Dict:
        """
        获取报告列表
        :param params:
        :return:
        """
        data = await UiReports.get_list(params)
        return data

    @staticmethod
    async def save_report(summary: TestCaseSummary,
                          run_type: str = 10,
                          project_id: int = None,
                          module_id: int = None,
                          env_id: int = None,
                          **kwargs: typing.Any
                          ) -> typing.Dict:
        """
        保存报告
        :param summary: 报告
        :param run_type: 运行类型， 同步 10 异步 20
        :param project_id: 项目id
        :param module_id:  模块id
        :param env_id: 环境id
        :return:
        """
        exec_user_id = kwargs.get("exec_user_id", None)
        exec_user_name = kwargs.get("exec_user_name", None)
        report_info = UiReportSaveSchema(
            name=summary.name,
            start_time=summary.start_time,
            duration=summary.duration,
            case_id=summary.case_id,
            run_type=run_type,
            success=summary.success,
            run_count=summary.run_count,
            actual_run_count=summary.actual_run_count,
            run_success_count=summary.run_success_count,
            run_fail_count=summary.run_fail_count,
            run_skip_count=summary.run_skip_count,
            run_err_count=summary.run_err_count,
            run_log=summary.log,
            project_id=project_id,
            module_id=module_id,
            env_id=env_id,
            exec_user_id=exec_user_id,
            exec_user_name=exec_user_name,
        )

        api_test_report = await UiReportService.save_report_info(report_info)
        await UiReportService.save_report_detail(summary, api_test_report.get("id"),
                                                 exec_user_id=exec_user_id,
                                                 exec_user_name=exec_user_name)

        return api_test_report

    @staticmethod
    async def save_report_info(params: UiReportSaveSchema):
        report_info = params.dict()
        api_test_report = await UiReports.create_or_update(report_info)
        return api_test_report

    @staticmethod
    async def save_report_detail(summary: TestCaseSummary, report_id: typing.Union[int, str], **kwargs: typing.Any):
        """
        报春报告详情
        :param summary: 报告结果
        :param report_id: 报告id
        :param kwargs: kwargs
        :return:
        """
        exec_user_id = kwargs.get("exec_user_id", None)
        exec_user_name = kwargs.get("exec_user_name", None)
        step_results = await UiReportService.parser_summary(summary.step_results)
        for result in step_results:
            report_detail_info = UiReportDetail.model(report_id)
            report_detail_info.id = None
            result["report_id"] = report_id
            result["exec_user_id"] = exec_user_id
            result["exec_user_name"] = exec_user_name
            await report_detail_info.create_or_update(result)

    @staticmethod
    async def parser_summary(step_results: typing.List[StepResult]) -> typing.List[typing.Dict]:
        step_results_list = []

        async def add_data(results: typing.List[StepResult]):
            nonlocal step_results_list
            data = await UiReportService.parser_summary(results)
            if data:
                step_results_list.extend(data)

        for result in step_results:
            """处理嵌套用例结果"""
            if result.step_result:
                await add_data(result.step_result)
            new_step = result.dict()
            if new_step.get("start_time", None):
                new_step["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_step["start_time"]))
            if result.ui_session_data:
                ui_session_data = result.ui_session_data
                if ui_session_data.screenshot_file_base64:
                    try:
                        file_info = await FileService.save_base64_file(ui_session_data.screenshot_file_base64,
                                                                       filename=f"{result.name}{get_time()}_screenshot.png")
                        new_step["screenshot_file_id"] = file_info.get("id", None)
                    except Exception as e:
                        logger.error(f"保存截图失败：{traceback.format_exc()}")
                new_step.update(result.ui_session_data.dict())
            step_results_list.append(new_step)

        return step_results_list

    @staticmethod
    async def deleted(params: UiReportId):
        """
        删除报告
        :param params:
        :return:
        """
        return await UiReports.delete(params.id)

    @staticmethod
    async def detail(params: UiReportDetailQuery) -> typing.Dict:
        """
        根据id获取报告详情
        :param params:
        :return:
        """
        report_detail = UiReportDetail.model(params.report_id)
        data = await report_detail.get_details(params)
        return data if data else []

    @staticmethod
    async def statistics(params: UiReportDetailQuery):
        """
        报告统计
        """
        report_detail = UiReportDetail.model(params.report_id)
        data = await report_detail.statistics(params)
        return data

    @staticmethod
    async def get_report_result(summary: TestCaseSummary,
                                project_id: int,
                                module_id: int,
                                env_id: int,
                                exec_user_id: int = None,
                                exec_user_name: str = None,
                                ) -> UiReportSaveSchema:
        ui_report_info = UiReportSaveSchema(
            name=summary.name,
            start_time=summary.start_time,
            duration=summary.duration,
            case_id=summary.case_id,
            run_type=10,
            success=summary.success,
            run_count=summary.run_count,
            actual_run_count=summary.actual_run_count,
            run_success_count=summary.run_success_count,
            run_fail_count=summary.run_fail_count,
            run_skip_count=summary.run_skip_count,
            run_err_count=summary.run_err_count,
            run_log=summary.log,
            project_id=project_id,
            module_id=module_id,
            env_id=env_id,
            exec_user_id=exec_user_id,
            exec_user_name=exec_user_name,
            updated_by=exec_user_id,
            created_by=exec_user_id,
        )
        return ui_report_info
