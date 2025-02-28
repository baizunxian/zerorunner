import typing

from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ApiCase, ApiCaseStep
from autotest.models.celery_beat_models import TimedTaskCase
from autotest.schemas.api.api_case import ApiCaseQuery, ApiCaseIn, ApiCaseId, TestCaseRun, ApiCaseIdsQuery, \
    ApiTestCaseRun, ApiCaseStepDataSchema
from autotest.schemas.step_data import TStepData
from autotest.services.api.api_report import ReportService
from autotest.services.api.run_handle_new import HandelTestCase
from autotest.utils.async_converter import sync_to_async
from autotest.utils.current_user import current_user
from autotest.utils.serialize import default_serialize
from autotest.utils.snowflake import IDCenter
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
        case_info = await ApiCase.get(params.id)
        if not params.version:
            params.version = 0
        if case_info:
            params.version = case_info.version + 1
            if case_info.name != params.name and exist_case_info:
                raise ParameterError("用例名以存在!")
        else:
            if exist_case_info:
                raise ParameterError("用例名以存在!")
        data = await ApiCase.create_or_update(params.dict(exclude={"step_data"}))
        tile_step_list = await ApiCaseService.tile_step_data(params.step_data, data.get("id"), data.get("version"))
        await ApiCaseStep.batch_create([step.dict() for step in tile_step_list])
        return data

    @staticmethod
    async def get_step_data_tree(step_list: typing.List[typing.Dict], parent_id: int = None) -> typing.List[TStepData]:
        step_tree = []
        if not step_list:
            return step_tree
        for step in step_list:
            new_step = TStepData.parse_obj(step)
            if new_step.parent_step_id == parent_id:
                children_steps = await ApiCaseService.get_step_data_tree(step_list, new_step.step_id)
                if children_steps:
                    new_step.children_steps = children_steps if children_steps else []
                step_ = new_step.dict()
                step_['api_name'] = step.get("api_name", None)
                step_['api_method'] = step.get("api_method", None)
                step_tree.append(step_)
        return step_tree

    @staticmethod
    async def tile_step_data(step_data: typing.List[TStepData],
                             case_id: typing.Union[str, int],
                             version: int,
                             parent_step_id: int = None) -> typing.List[ApiCaseStepDataSchema]:
        """处理用例步骤数据"""
        tile_step_list = []
        for step in step_data:
            step.case_id = case_id
            step.version = version
            step.step_id = IDCenter.get_id()
            step.parent_step_id = parent_step_id
            # if step.step_type.lower() == TStepTypeEnum.api.value:
            #     step.url = step.request.url
            #     step.method = step.request.method
            tile_step_list.append(step)
            if step.children_steps:
                tile_step_list.extend(
                    await ApiCaseService.tile_step_data(step.children_steps, case_id, version, step.step_id))
        return tile_step_list

    @staticmethod
    async def deleted(params: ApiCaseId):
        """删除用例"""
        return await ApiCase.delete(params.id)

    @staticmethod
    async def get_case_info(params: ApiCaseId) -> typing.Dict:
        """获取用例信息"""
        api_case = await ApiCase.get(params.id, to_dict=True)
        await ApiCaseService.set_step_data(api_case)
        if not api_case:
            raise ValueError('不存在当前套件！')
        return api_case

    @staticmethod
    async def set_step_data(api_case: typing.Dict):
        step_data = await ApiCaseStep.get_step_by_case_id(api_case["id"], api_case["version"])
        step_data_tree = await ApiCaseService.get_step_data_tree(step_data)
        api_case["step_data"] = step_data_tree

    @staticmethod
    async def run_case(params: ApiTestCaseRun):
        """运行用例"""
        if not params.id:
            raise ValueError("id 不能为空！")
        case_info = await ApiCase.get(params.id, to_dict=True)
        await ApiCaseService.set_step_data(case_info)
        run_params = TestCaseRun(**default_serialize(case_info), env_id=params.env_id)
        api_case_info = await HandelTestCase().init(run_params)
        runner = ZeroRunner()
        testcase = api_case_info.get_testcases()
        summary = await runner.run_tests(testcase)
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
        summary = await sync_to_async(runner.run_tests, testcase)
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

    @staticmethod
    def run_callback(*args, **kwargs):
        print(1111)
        ...

    @staticmethod
    async def use_case_relation(params: ApiCaseId):
        api_info = await ApiCase.get_api_by_id(params.id)
        if not api_info:
            raise ValueError('不存在当前用例！')
        relation_timed_task_ids = set()
        line_list = []
        node_list = [dict(id=f"case_{params.id}",
                          data=dict(id=params.id,
                                    type="case",
                                    name=api_info.get("name"),
                                    created_by_name=api_info.get("created_by_name"),
                                    creation_date=api_info.get("creation_date")))]
        # case - timed task 关联
        timed_task_case_list = await TimedTaskCase.get_relation_by_case_ids([params.id]) or []
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
            "timed_task_count": len(relation_timed_task_ids)
        }
        return data
