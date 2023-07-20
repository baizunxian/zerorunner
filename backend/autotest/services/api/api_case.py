import typing

from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ApiCase
from autotest.schemas.api.api_case import ApiCaseQuery, ApiCaseIn, ApiCaseId, TestCaseRun, ApiCaseIdsQuery, \
    ApiTestCaseRun
from autotest.services.api.run_handle import ApiCaseHandle
from autotest.services.api.run_handle_new import HandelTestCase
from autotest.services.api.api_report import ReportService
from autotest.utils import current_user
from autotest.corelibs.serialize import default_serialize
from zerorunner.testcase_new import ZeroRunner


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
    async def run_case(params: ApiTestCaseRun):
        """运行用例"""
        if not params.id:
            raise ValueError("id 不能为空！")
        case_info = await ApiCase.get(params.id)
        run_params = TestCaseRun(**default_serialize(case_info), env_id=params.env_id)
        api_case_info = await ApiCaseHandle.init(run_params)
        await api_case_info.make_functions()
        runner = ZeroRunner()
        testcase = api_case_info.get_testcase()
        summary = runner.run_tests(testcase)
        current_user_info = await current_user()
        summary_params = await ReportService.get_report_result(summary,
                                                               api_case_info.api_case.project_id,
                                                               api_case_info.api_case.module_id,
                                                               api_case_info.api_case.env_id,
                                                               ex_user_id=current_user_info.get("id", None))
        report_info = await ReportService.save_report_info(summary_params)
        report_id = report_info.get("id")
        await ReportService.save_report_detail(summary, report_id)
        return report_info

    @staticmethod
    async def debug_case(params: TestCaseRun):
        """调试用例"""
        case_info = await HandelTestCase().init(params)
        runner = ZeroRunner()
        # case_info.make_functions()
        testcase = case_info.get_testcases()
        summary = runner.run_tests(testcase)
        # summary = runner.get_summary()
        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id
        # report_info = await ReportService.save_report(summary, project_id=project_id, module_id=module_id, env_id=env_id)
        return summary

    @staticmethod
    def case_summary_to_report(summary):

        params_dict = (
            dict(run_count=summary.run_count,
                 run_success_count=summary.run_success_count,
                 run_skip_count=summary.run_skip_count,
                 run_fail_count=summary.run_fail_count,
                 run_err_count=summary.run_err_count,
                 duration=summary.duration,
                 start_time=summary.start_time,
                 actual_run_count=summary.actual_run_count)
        )
        report_info.update(params_dict)
        summary_params = TestReportSaveSchema(**report_info)

    @staticmethod
    async def get_count_by_user():
        """获取用户用例数量"""
        user_info = await current_user()
        count_info = await ApiCase.get_count_by_user_id(user_info.get("id", None))
        if not count_info:
            return 0
        if count_info:
            return count_info.get("count", 0)
