from typing import Dict, Any, Union, Text

from autotest.models.api_models import ApiSuite
from autotest.serialize.api_serializes.api_suites import ApiSuitesListSchema, ApiSuitesQuerySchema, \
    ApiSuitesSaveSchema
from autotest.services.api_services.run_handle import ApiSuiteHandle
from autotest.services.api_services.test_report import ReportService
from autotest.utils.api import parse_pagination
from zerorunner.models import TestCase
from zerorunner.runner import ZeroRunner


class ApiSuitesService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = ApiSuitesQuerySchema(**kwargs).dict()
        data = parse_pagination(ApiSuite.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': ApiSuitesListSchema.serialize(_result)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "ApiSuite":
        """更新保存套件"""
        parsed_data = ApiSuitesSaveSchema(**kwargs)
        #  套件名称唯一性校验
        test_suite = ApiSuite.get(parsed_data.id) if parsed_data.id else ApiSuite()
        test_suite.update(**parsed_data.dict())
        return test_suite

    @staticmethod
    def deleted(s_id: Union[str, int]):
        test_suite = ApiSuite.get(s_id)
        test_suite.delete() if test_suite else ...

    @staticmethod
    def get_suite_info(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = ApiSuitesQuerySchema(**kwargs)
        api_suite = ApiSuite.get(parsed_data.id) if parsed_data.id else None
        if api_suite:
            return api_suite
        raise ValueError('不存在当前套件！')

    @staticmethod
    def run_suites(**kwargs: Any):
        zr = ZeroRunner()
        suite_info = ApiSuiteHandle(**kwargs)
        test_case = TestCase(config=suite_info.config, teststeps=suite_info.teststeps)
        zr.run_testcase(test_case)
        summary = zr.get_summary()
        project_id = suite_info.api_suites.project_id
        module_id = suite_info.api_suites.module_id
        env_id = suite_info.api_suites.env_id
        report_info = ReportService.save_report(summary, project_id, module_id, env_id)

    @staticmethod
    def debug_suites(**kwargs: Any):
        zr = ZeroRunner()
        suite_info = ApiSuiteHandle(**kwargs)
        test_case = TestCase(config=suite_info.config, teststeps=suite_info.teststeps)
        zr.run_testcase(test_case)
        summary = zr.get_summary()
        project_id = suite_info.api_suites.project_id
        module_id = suite_info.api_suites.module_id
        env_id = suite_info.api_suites.env_id
        report_info = ReportService.save_report(summary, project_id, module_id, env_id)
        return report_info
