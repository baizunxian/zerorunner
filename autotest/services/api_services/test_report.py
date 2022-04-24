import json
import time
from typing import Dict, Any, NoReturn

from autotest.serialize.api_serializes.test_report import (
    TestReportQuerySchema, ReportsListSchema, TestReportSaveSchema,
    TestReportMakeSchema, ReportsLInfoSchema)
from autotest.models.api_models import TestReports
from autotest.utils.api import parse_pagination


class ReportService:

    @staticmethod
    def list(**kwargs: Any) -> Dict:
        parsed_data = TestReportQuerySchema().load(kwargs)
        data = parse_pagination(TestReports.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')

        # test_count = i['test_count']
        # batch_id = i['id']
        # # 如果运行用例数还没有回写，就去redis中查询
        # if test_count is None:
        #     statis_key = TEST_EXECUTE_STATIS.format(batch_id)
        # ex_count = br.hget(statis_key, 'ex_count') if br.hget(statis_key, 'ex_count') else 0
        # start_datetime = br.hget(statis_key, 'start_datetime')
        # i['test_count'] = ex_count
        # i['start_at'] = start_datetime

        result = {
            'rows': ReportsListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def make_report(**kwargs: Any) -> Dict:
        report_body = TestReportMakeSchema().load(kwargs)
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
    def save_report(**kwargs: Any):
        report_body = TestReportSaveSchema().load(kwargs)
        test_report = TestReports()
        test_report.update(**report_body)

    @staticmethod
    def deleted(report_id: int) -> NoReturn:
        test_reports = TestReports.get(report_id)
        test_reports.deleted() if test_reports else ...

    @staticmethod
    def get_report_by_id(report_id: int) -> Dict:
        report_info = TestReports.get(report_id)
        return ReportsLInfoSchema().dump(report_info)
