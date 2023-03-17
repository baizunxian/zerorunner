import time
import typing

from autotest.models.api_models import ApiTestReport, ApiTestReportDetail
from autotest.schemas.api.test_report import TestReportQuery, TestReportId, TestReportDetailQuery, TestReportSaveSchema
from zerorunner.models import TestCaseSummary, StepData


class ReportService:

    @staticmethod
    async def list(params: TestReportQuery) -> typing.Dict:
        """
        获取报告列表
        :param params:
        :return:
        """
        data = await ApiTestReport.get_list(params)
        return data

    @staticmethod
    async def save_report(params: TestReportSaveSchema) -> typing.Dict:
        """
        保存报告
        :param params: 参数
        :return:
        """
        # report_info = TestReportSaveSchema(
        #     name=summary.name,
        #     start_time=summary.start_time,
        #     duration=summary.duration,
        #     case_id=summary.case_id,
        #     run_mode="case",
        #     run_type=10,
        #     success=summary.success,
        #     run_count=summary.run_count,
        #     actual_run_count=summary.actual_run_count,
        #     run_success_count=summary.run_success_count,
        #     run_fail_count=summary.run_fail_count,
        #     run_skip_count=summary.run_skip_count,
        #     run_err_count=summary.run_err_count,
        #     run_log=summary.log,
        #     project_id=project_id,
        #     module_id=module_id,
        #     env_id=env_id
        # )

        report_info = params.dict()
        api_test_report = await ApiTestReport.create_or_update(report_info)
        return api_test_report

    @staticmethod
    async def save_report_detail(summary: typing.Any, report_id: typing.Union[int, str]):
        """
        报春报告详情
        :param summary: 报告结果
        :param report_id: 报告id
        :return:
        """

        step_data_list = ReportService.parser_summary(summary.step_datas)
        for step_detail in step_data_list:
            report_detail_info = ApiTestReportDetail.model(report_id)
            report_detail_info.id = None
            step_detail["report_id"] = report_id
            await report_detail_info.create_or_update(step_detail)

    @staticmethod
    def parser_summary(step_datas: typing.List[StepData]) -> typing.List[typing.Dict]:
        step_data_list = []

        def add_data(step_data: typing.List[StepData]):
            nonlocal step_data_list
            data = ReportService.parser_summary(step_data)
            if data:
                step_data_list.extend(data)

        for step in step_datas:
            if step.step_data:
                add_data(step.step_data)
            # if step.pre_hook_data:
            #     add_data(step.pre_hook_data)
            # if step.post_hook_data:
            #     add_data(step.post_hook_data)

            new_step = step.dict()
            # new_step = step.dict(exclude={"step_data"})
            if new_step.get("start_time", None):
                new_step["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_step["start_time"]))
            if step.session_data:
                if step.session_data.req_resp:
                    new_step["url"] = step.session_data.req_resp.request.url
                    new_step["method"] = step.session_data.req_resp.request.method
                    new_step["status_code"] = step.session_data.req_resp.response.status_code
                    new_step["response_time_ms"] = step.session_data.stat.response_time_ms
                    new_step["elapsed_ms"] = step.session_data.stat.elapsed_ms
            step_data_list.append(new_step)

        return step_data_list

    @staticmethod
    async def deleted(params: TestReportId):
        """
        删除报告
        :param params:
        :return:
        """
        return await ApiTestReport.delete(params.id)

    @staticmethod
    async def detail(params: TestReportDetailQuery) -> typing.Dict:
        """
        根据id获取报告详情
        :param params:
        :return:
        """
        report_detail = ApiTestReportDetail.model(params.id)
        data = await report_detail.get_list(params)
        return data

    @staticmethod
    async def statistics(params: TestReportDetailQuery):
        """
        报告统计
        """
        report_detail = ApiTestReportDetail.model(params.id)
        data = await report_detail.statistics(params)
        return data

    @staticmethod
    async def get_report_result(summary: TestCaseSummary, project_id: int, module_id: int,
                                env_id: int) -> TestReportSaveSchema:
        report_info = TestReportSaveSchema(
            name=summary.name,
            start_time=summary.start_time,
            duration=summary.duration,
            case_id=summary.case_id,
            run_mode="case",
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
            env_id=env_id
        )
        return report_info
