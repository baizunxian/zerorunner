import typing

from loguru import logger

from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ApiInfo, ApiCaseStep, ApiCaseStep
from autotest.models.celery_beat_models import TimedTaskCase
from autotest.schemas.api.api_info import ApiQuery, ApiId, ApiInfoIn, ApiRunSchema, ApiIds
from autotest.services.api.api_report import ReportService
from autotest.services.api.run_handle_new import HandelRunApiStep
from autotest.utils.current_user import current_user
from autotest.utils.serialize import default_serialize
from celery_worker.tasks import test_case
from zerorunner.testcase import ZeroRunner


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
        # zero = Zero()
        # if params.setup_code:
        #     mod = load_script_content(params.setup_code, str(uuid.uuid4()), params={"zero": zero})
        # if params.teardown_code:
        #     mod = load_script_content(params.teardown_code, str(uuid.uuid4()), params={"zero": zero})
        # if mod:
        #     del mod

        if params.id:
            api_info = await ApiInfo.get(params.id)
            if not api_info:
                raise ParameterError("用例不存在!")
            if api_info.name != params.name:
                if existing_data:
                    raise ParameterError("用例名重复!")
        data = await ApiInfo.create_or_update(params.dict())
        return await ApiInfo.get_api_by_id(data.get('id', None))

    @staticmethod
    async def copy_api(params: ApiId):
        source_api_info = await ApiInfo.get(params.id, to_dict=True)
        if not source_api_info:
            raise ParameterError("用例不存在!")
        source_api_info.pop("id", None)
        api_info = ApiInfoIn.parse_obj(source_api_info)
        api_info.id = None
        api_info.name = f"copy_{api_info.name}"
        await ApiInfoService.save_or_update(api_info)

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
    async def get_detail_by_ids(params: ApiIds) -> typing.Dict:
        """
        根据用例ids获取用例信息
        :param params:
        :return:
        """
        api_info_list = await ApiInfo.get_api_by_ids(params)

        return api_info_list if api_info_list else []

    @staticmethod
    async def run_api(params: ApiRunSchema):
        """"""
        current_user_info = await current_user()
        params.exec_user_id = current_user_info.get("id", None)
        params.exec_user_name = current_user_info.get("nickname", None)
        if params.api_run_mode == "one":
            if params.run_mode == 20:
                logger.info('异步执行用例 ~')
                test_case.async_run_api.apply_async(kwargs=params.dict(), __business_id=params.id)
            else:
                summary = await ApiInfoService.run(params)  # 初始化校验，避免生成用例是出错
                return summary
        else:
            logger.info('批量运行用例 ~')
            for id_ in params.ids:
                new_params = ApiRunSchema(
                    id=id_,
                    env_id=params.env_id,
                    name=params.name,
                    run_type=params.run_type,
                    run_mode=params.run_mode,
                    number_of_run=params.number_of_run,
                    exec_user_id=params.exec_user_id,
                    exec_user_name=params.exec_user_name
                )
                if params.run_type == 20:
                    logger.info('异步执行用例 ~')
                    test_case.async_run_api.apply_async(kwargs=new_params.dict(), __business_id=params.id)
                else:
                    await ApiInfoService.run(new_params)  # 初始化校验，避免生成用例是出错

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
                                                      run_mode=params.run_mode,
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
            parsed_data = ApiInfoIn.parse_obj(case).dict()
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

    @staticmethod
    async def use_api_relation(params: ApiId):
        """
        api使用关系
        :param params:
        :return:
        """
        api_info = await ApiInfo.get_api_by_id(params.id)
        if not api_info:
            raise ValueError('不存在当前接口！')
        line_list = []
        relation_case_ids = set()
        relation_timed_task_ids = set()

        # api关联到的测试用例
        api_case_relation_data = await ApiCaseStep.get_relation_by_api_id(params.id) or []
        node_list = [dict(id=f"api_{params.id}",
                          data=dict(id=params.id,
                                    type="api",
                                    name=api_info.get("name"),
                                    created_by_name=api_info.get("created_by_name"),
                                    creation_date=api_info.get("creation_date")))]

        for relation_data in api_case_relation_data:
            case_id = relation_data.get("case_id")
            relation_id = f"case_{case_id}"
            node_data = dict(id=relation_id,
                             data=dict(id=case_id,
                                       type="case",
                                       created_by_name=relation_data.get("created_by_name"),
                                       creation_date=relation_data.get("creation_date"),
                                       name=relation_data.get("case_name")))
            relation_case_ids.add(case_id)
            node_list.append(node_data)
            line_list.append({
                "from": f"api_{params.id}",
                "to": relation_id,
                "text": "关联用例"
            })

        # case - timed task 关联
        timed_task_case_list = await TimedTaskCase.get_relation_by_case_ids(list(relation_case_ids)) or []
        for timed_task_case in timed_task_case_list:
            task_id = timed_task_case.get('id')
            case_id = timed_task_case.get("case_id")
            relation_id = f"timed_task_{task_id}"
            node_data = dict(id=relation_id,
                             data=dict(id=task_id,
                                       type="timed_task",
                                       name=timed_task_case.get("task_name"),
                                       created_by_name=timed_task_case.get("created_by_name"),
                                       creation_date=timed_task_case.get("creation_date")))
            node_list.append(node_data)
            line_list.append({
                "from": f"case_{case_id}",
                "to": relation_id,
                "text": "关联定时任务"
            })
            relation_timed_task_ids.add(task_id)

        data = {
            "rootId": f"api_{params.id}",
            "nodes": node_list,
            "lines": line_list,
            "case_count": len(relation_case_ids),
            "timed_task_count": len(relation_timed_task_ids)
        }
        return data
