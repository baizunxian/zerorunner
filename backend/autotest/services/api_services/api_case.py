from typing import Dict, Any, Union, Text

from autotest.models.api_models import ApiCase
from autotest.serialize.api_serializes.api_case import ApiCaseListSchema, ApiCaseQuerySchema, \
    ApiCaseSaveSchema
from autotest.services.api_services.run_handle import ApiCaseHandle, Runner
from autotest.services.api_services.test_report import ReportService
from autotest.utils.api import parse_pagination, jsonable_encoder
from zerorunner.testcase import ZeroRunner


class ApiCaseService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """用例列表"""
        parsed_data = ApiCaseQuerySchema(**kwargs).dict()
        data = parse_pagination(ApiCase.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': ApiCaseListSchema.serialize(_result)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "ApiCase":
        """用例保存"""
        parsed_data = ApiCaseSaveSchema(**kwargs)
        #  套件名称唯一性校验
        test_suite = ApiCase.get(parsed_data.id) if parsed_data.id else ApiCase()
        test_suite.update(**parsed_data.dict())
        return test_suite

    @staticmethod
    def deleted(s_id: Union[str, int]):
        """删除用例"""
        test_suite = ApiCase.get(s_id)
        test_suite.delete() if test_suite else ...

    @staticmethod
    def get_case_info(**kwargs: Any) -> Dict[Text, Any]:
        """获取用例信息"""
        parsed_data = ApiCaseQuerySchema(**kwargs)
        api_suite = ApiCase.get(parsed_data.id) if parsed_data.id else None
        if api_suite:
            return api_suite
        raise ValueError('不存在当前套件！')

    @staticmethod
    def run_case(**kwargs: Any):
        """运行用例"""
        case_id = kwargs.get("id", None)
        if not case_id:
            raise ValueError("id 不能为空！")
        case_info = ApiCase.get(case_id)
        case_info = ApiCaseHandle(**jsonable_encoder(case_info))
        runner = Runner(case_info.get_testcase())
        runner.run()
        summary = runner.get_summary()
        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id
        report_info = ReportService.save_report(summary, project_id, module_id, env_id)
        return report_info

    @staticmethod
    def debug_case(**kwargs: Any):
        """调试用例"""
        case_info = ApiCaseHandle(**kwargs)
        runner = ZeroRunner()
        runner.run_tests(case_info.get_testcase())
        summary = runner.get_summary()
        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id
        report_info = ReportService.save_report(summary, project_id, module_id, env_id)
        return report_info
