import time
import typing

from autotest.models.api_models import ApiTestReport, ApiTestReportDetail
from autotest.schemas.api.test_report import TestReportQuery, TestReportId, TestReportDetailQuery, TestReportSaveSchema
from zerorunner.model.result_model import TestCaseSummary, StepResult


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
    async def save_report(summary: TestCaseSummary,
                          run_mode: str = "case",
                          run_type: int = 10,
                          project_id: int = None,
                          module_id: int = None,
                          env_id: int = None) -> typing.Dict:
        """
        保存报告
        :param summary: 报告
        :param run_mode: 运行模式  case api
        :param run_type: 运行类型， 同步 10 异步 20
        :param project_id: 项目id
        :param module_id:  模块id
        :param env_id: 环境id
        :return:
        """
        report_info = TestReportSaveSchema(
            name=summary.name,
            start_time=summary.start_time,
            duration=summary.duration,
            case_id=summary.case_id,
            run_mode=run_mode,
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
            env_id=env_id
        )

        api_test_report = await ReportService.save_report_info(report_info)
        await ReportService.save_report_detail(summary, api_test_report.get("id"))

        return api_test_report

    @staticmethod
    async def save_report_info(params: TestReportSaveSchema):
        report_info = params.dict()
        api_test_report = await ApiTestReport.create_or_update(report_info)
        return api_test_report

    @staticmethod
    async def save_report_detail(summary: TestCaseSummary, report_id: typing.Union[int, str]):
        """
        报春报告详情
        :param summary: 报告结果
        :param report_id: 报告id
        :return:
        """

        step_results = ReportService.parser_summary(summary.step_results)
        for result in step_results:
            report_detail_info = ApiTestReportDetail.model(report_id)
            report_detail_info.id = None
            result["report_id"] = report_id
            await report_detail_info.create_or_update(result)

    @staticmethod
    def parser_summary(step_results: typing.List[StepResult]) -> typing.List[typing.Dict]:
        step_results_list = []

        def add_data(results: typing.List[StepResult]):
            nonlocal step_results_list
            data = ReportService.parser_summary(results)
            if data:
                step_results_list.extend(data)

        for result in step_results:
            if result.step_result:
                add_data(result.step_result)
            # if step.pre_hook_data:
            #     add_data(step.pre_hook_data)
            # if step.post_hook_data:
            #     add_data(step.post_hook_data)

            new_step = result.dict()
            # new_step = step.dict(exclude={"step_data"})
            if new_step.get("start_time", None):
                new_step["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_step["start_time"]))
            if result.session_data:
                if result.session_data.req_resp:
                    new_step["url"] = result.session_data.req_resp.request.url
                    new_step["method"] = result.session_data.req_resp.request.method
                    new_step["status_code"] = result.session_data.req_resp.response.status_code
                    new_step["response_time_ms"] = result.session_data.stat.response_time_ms
                    new_step["elapsed_ms"] = result.session_data.stat.elapsed_ms
            step_results_list.append(new_step)

        return step_results_list

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
