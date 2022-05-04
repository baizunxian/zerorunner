import json
from typing import Dict, Any, Text

from autotest.models.api_models import TestReports
from autotest.serialize.api_serializes.test_report import (
    TestReportQuerySchema, ReportsListSchema, TestReportSaveSchema,
    TestReportMakeSchema, ReportsLInfoSchema)
from autotest.utils.api import parse_pagination


class ReportService:

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取报告列表
        :param kwargs:
        :return:
        """
        parsed_data = TestReportQuerySchema().load(kwargs)
        data = parse_pagination(TestReports.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')

        result = {
            'rows': ReportsListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def make_report(summary: Any) -> Dict[Text, Any]:
        """
        处理报告
        :param summary:
        :return:
        """
        report_body = TestReportMakeSchema().load(summary)
        time_dict = report_body['time']
        teststeps_info = report_body['stat'].get('teststeps', {})

        return dict(
            name='',
            start_at=time_dict.get('start_at'),
            scene_num=0,
            duration=str(round(time_dict.get('duration'), 2)),
            run_type=None,
            task_type=None,
            project_id=None,
            module_id=None,
            report_type=None,
            run_case_priority=None,
            execute_service=None,
            execute_source=None,
            execute_user_id=None,
            successful_use_case=teststeps_info.get('successes', 0),
            success=report_body.get('success'),
            run_test_count=teststeps_info.get('total', 0),
            report_body=json.dumps(report_body),
        )

    @staticmethod
    def save_report(**kwargs: Any) -> "TestReports":
        """
        保存报告
        :param kwargs:
        :return:
        """
        report_body = TestReportSaveSchema().load(kwargs)
        test_report = TestReports()
        test_report.update(**report_body)
        return test_report

    @staticmethod
    def deleted(report_id: int):
        """
        删除报告
        :param report_id:
        :return:
        """
        test_reports = TestReports.get(report_id)
        test_reports.deleted() if test_reports else ...

    @staticmethod
    def get_report_by_id(report_id: int) -> Dict[Text, Any]:
        """
        根据id获取报告详情
        :param report_id:
        :return:
        """
        report_info = TestReports.get(report_id)
        return ReportsLInfoSchema().dump(report_info)
