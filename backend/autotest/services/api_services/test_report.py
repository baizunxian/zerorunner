import time
from typing import Dict, Any, Text, List

from autotest.models.api_models import ApiTestReport, ApiTestReportDetail
from autotest.serialize.api_serializes.test_report import (
    TestReportQuerySchema, TestReportSaveSchema)
from autotest.utils.api import parse_pagination, jsonable_encoder
from zerorunner.models import TestCaseSummary, StepData


class ReportService:

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取报告列表
        :param kwargs:
        :return:
        """
        parsed_data = TestReportQuerySchema(**kwargs).dict()
        data = parse_pagination(ApiTestReport.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_report_detail(summary: Any) -> Dict[Text, Any]:
        """
        处理报告
        :param summary:
        :return:
        """

        ...

    @staticmethod
    def save_report(summary: TestCaseSummary, project_id: int, module_id: int, env_id: int) -> "ApiTestReport":
        """
        保存报告
        :param summary: 测试报告
        :param project_id: 项目id
        :param module_id: 模块id
        :param env_id: 环境id
        :return:
        """
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

        summary_list = ReportService.parser_summary(summary.step_datas)

        test_report = ApiTestReport()
        test_report.update(**report_info.dict())

        for step_detail in summary_list:
            report_detail_info = ApiTestReportDetail.model(test_report.id)
            report_detail_info.id = None
            step_detail["report_id"] = test_report.id
            report_detail_info.update(**step_detail)

        return test_report

    @staticmethod
    def parser_summary(step_datas: List[StepData]) -> List[Dict[Text, Any]]:
        step_data_list = []

        def add_data(step_data: List[StepData]):
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
                new_step["status_code"] = step.session_data.req_resp.response.status_code
                new_step["response_time_ms"] = step.session_data.stat.response_time_ms
                new_step["elapsed_ms"] = step.session_data.stat.elapsed_ms
            step_data_list.append(jsonable_encoder(new_step))

        return step_data_list

    @staticmethod
    def deleted(report_id: int):
        """
        删除报告
        :param report_id:
        :return:
        """
        test_reports = ApiTestReport.get(report_id)
        test_reports.deleted() if test_reports else ...

    @staticmethod
    def detail(report_id: int, parent_step_id=None) -> Dict[Text, Any]:
        """
        根据id获取报告详情
        :param report_id:
        :return:
        """
        report_detail = ApiTestReportDetail.model(report_id)
        data = parse_pagination(report_detail.get_list(report_id, parent_step_id))
        _result, pagination = data.get('result'), data.get('pagination')
        for res in _result:
            res["has_step_data"] = report_detail.get_list(report_id, res["step_id"]).count()
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def statistics(report_id: int, parent_step_id=None):
        """
        报告统计
        """
        report_detail = ApiTestReportDetail.model(report_id)
        data = report_detail.statistics(report_id, parent_step_id)
        return data
