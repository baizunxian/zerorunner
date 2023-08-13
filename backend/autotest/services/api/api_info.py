import typing
import uuid

from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ApiInfo
from autotest.schemas.api.api_info import ApiQuery, ApiId, ApiInfoIn, ApiRunSchema
from autotest.services.api.run_handle_new import HandelRunApiStep
from autotest.services.api.api_report import ReportService
from autotest.corelibs.serialize import default_serialize
from autotest.utils import current_user
from zerorunner.loader import load_script_content
from zerorunner.script_code import Zero
from zerorunner.testcase_new import ZeroRunner


class ApiInfoService:
    @staticmethod
    async def list(params: ApiQuery) -> typing.Dict:
        """
        接口列表
        :param params:
        :return:
        """
        data = await ApiInfo.get_list(params)
        return data

    @staticmethod
    async def save_or_update(params: ApiInfoIn) -> typing.Dict:
        """
        更新保存测试用例/配置
        :param params:
        :return:
        """
        if not params.name:
            raise ParameterError("用例名不能为空!")
        # 判断用例名是否重复
        existing_data = await ApiInfo.get_api_by_name(name=params.name)
        mod = None
        zero = Zero()
        if params.setup_code:
            mod = load_script_content(params.setup_code, str(uuid.uuid4()), params={"zero": zero})
        if params.teardown_code:
            mod = load_script_content(params.teardown_code, str(uuid.uuid4()), params={"zero": zero})
        if mod:
            del mod

        if params.id:
            api_info = await ApiInfo.get(params.id)
            if not api_info:
                raise ParameterError("用例不存在!")
            if api_info.name != params.name:
                if existing_data:
                    raise ParameterError("用例名重复!")

        return await ApiInfo.create_or_update(params.dict())

    @staticmethod
    async def set_api_status(**kwargs: typing.Any):
        """
        用例失效生效
        :param kwargs:
        :return:
        """
        ids = kwargs.get('ids', None)
        case_list = ApiInfo.get_list(ids=ids).all()
        for case_info in case_list:
            case_info.case_status = 20 if case_info.case_status == 10 else 10
            case_info.save()

    @staticmethod
    async def deleted(id: typing.Union[int, str]):
        """
        删除api
        :param id:
        :return:
        """
        return await ApiInfo.delete(id=id)

    @staticmethod
    async def detail(params: ApiId) -> typing.Dict:
        """
        获取用例信息
        :param params:
        :return:
        """
        api_info = await ApiInfo.get_api_by_id(params.id)
        if not api_info:
            raise ValueError('当前用例不存在！')
        return api_info

    @staticmethod
    async def run(params: ApiRunSchema, **kwargs) -> typing.Dict:
        """
        运行测试用例
        :param params:
        :param kwargs:
        :return:
        """
        case_info = await ApiInfo.get(params.id)
        run_params = ApiInfoIn(**default_serialize(case_info), env_id=params.env_id)
        case_info = await HandelRunApiStep().init(run_params)
        runner = ZeroRunner()
        summary = runner.run_tests(case_info.get_testcase())
        report_info = await ReportService.save_report(summary=summary,
                                                      run_mode='api',
                                                      run_type=params.run_type,
                                                      project_id=case_info.api_info.project_id,
                                                      module_id=case_info.api_info.module_id,
                                                      env_id=case_info.api_info.env_id,
                                                      exec_user_id=params.exec_user_id,
                                                      exec_user_name=params.exec_user_name,
                                                      )
        return report_info

    @staticmethod
    async def debug_api(params: ApiInfoIn) -> typing.Any:
        """
        用例调试
        :param params:
        :return:
        """
        case_info = await HandelRunApiStep().init(params)
        runner = ZeroRunner()
        print(id(runner))
        summary = runner.run_tests(case_info.get_testcase())

        return summary

    @staticmethod
    def postman2api(json_body: typing.Dict, **kwargs):
        """postman 转 api"""
        coll = Collection(json_body)
        coll.make_test_case()
        for testcase in coll.case_list:
            case = {
                "name": testcase.name,
                "priority": 3,
                "code": kwargs.get('code', ''),
                "project_id": kwargs.get('project_id', None),
                "module_id": kwargs.get('module_id', None),
                "service_name": kwargs.get('service_name', ''),
                "config_id": kwargs.get('config_id', None),
                "user_id": get_user_id_by_token(),
                "testcase": testcase.dict(),
            }
            parsed_data = ApiInfoIn(**case).dict()
            case_info = ApiInfo()
            case_info.update(**parsed_data)
        return len(coll.case_list)

    @staticmethod
    async def get_count_by_user():
        """获取用户api数量"""
        user_info = await current_user()
        count_info = await ApiInfo.get_count_by_user_id(user_info.get("id", None))
        if not count_info:
            return 0
        if count_info:
            return count_info.get("count", 0)
