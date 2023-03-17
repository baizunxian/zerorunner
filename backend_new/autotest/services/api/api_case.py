import typing

from autotest.exceptions import ParameterError
from autotest.models.api_models import ApiCase
from autotest.schemas.api.api_case import ApiCaseQuery, ApiCaseIn, ApiCaseId, ApiCaseRun, ApiCaseIdsQuery
from autotest.schemas.api.test_report import TestReportSaveSchema
from autotest.services.api.run_handle import ApiCaseHandle
from autotest.services.api.test_report import ReportService
from autotest.utils.serialize import default_serialize
from zerorunner.testcase import ZeroRunner


class ApiCaseService:
    @staticmethod
    async def list(params: ApiCaseQuery) -> typing.Dict:
        """用例列表"""
        result = await ApiCase.get_list(params)
        for data in result:
            if 'include' in data:
                data['include'] = list(map(int, data['include'].split(','))) if data['include'] else []
        return result

    @staticmethod
    async def get_case_by_ids(params: ApiCaseIdsQuery) -> typing.Dict:
        """用例列表"""
        result = await ApiCase.get_case_by_ids(ids=params.ids)
        return result

    @staticmethod
    async def save_or_update(params: ApiCaseIn) -> typing.Dict:
        """用例保存"""
        # 判断用例名是否重复
        exist_case_info = await ApiCase.get_case_by_name(name=params.name)
        if params.id:
            case_info = await ApiCase.get(params.id)
            if case_info.name != params.name and exist_case_info:
                raise ParameterError("套件名以存在!")
        else:
            if exist_case_info:
                raise ParameterError("套件名以存在!")
        data = await ApiCase.create_or_update(params.dict())
        return data

    @staticmethod
    async def deleted(params: ApiCaseId):
        """删除用例"""
        return await ApiCase.delete(params.id)

    @staticmethod
    async def get_case_info(params: ApiCaseId) -> typing.Dict:
        """获取用例信息"""
        api_case = await ApiCase.get(params.id)
        if not api_case:
            raise ValueError('不存在当前套件！')
        return api_case

    @staticmethod
    async def run_case(params: ApiCaseId):
        """运行用例"""
        if not params.id:
            raise ValueError("id 不能为空！")
        case_info = await ApiCase.get(params.id)
        run_params = ApiCaseRun(**default_serialize(case_info))
        api_case_info = await ApiCaseHandle.init(run_params)
        await api_case_info.make_functions()
        runner = ZeroRunner()
        testcase = api_case_info.get_testcase()
        summary = runner.run_tests(testcase)
        summary_params = await ReportService.get_report_result(summary,
                                                               api_case_info.api_case.project_id,
                                                               api_case_info.api_case.module_id,
                                                               api_case_info.api_case.env_id)
        report_info = await ReportService.save_report(summary_params)
        report_id = report_info.get("id")
        await ReportService.save_report_detail(summary, report_id)
        return report_info

    @staticmethod
    async def debug_case(params: ApiCaseRun):
        """调试用例"""
        case_info = await ApiCaseHandle.init(params)
        runner = ZeroRunner()
        testcase = case_info.get_testcase()
        summary = runner.run_tests(testcase)
        # summary = runner.get_summary()
        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id
        # report_info = ReportService.save_report(summary, project_id, module_id, env_id)
        return summary
