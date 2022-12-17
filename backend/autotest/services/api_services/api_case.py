import json
from typing import Dict, Any, Union, Text
from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.models.api_models import ApiCase
from autotest.serialize.api_serializes.api_case import (CaseQuerySchema, CaseSaveOrUpdateSchema)
from autotest.services.api_services.run_handle import ApiCaseHandle
from autotest.services.api_services.test_report import ReportService
from autotest.services.utils_services.postman2case import Collection
from autotest.utils.api import parse_pagination, jsonable_encoder
from autotest.utils.common import get_user_id_by_token
from zerorunner.models import TestCase
from zerorunner.runner import ZeroRunner


class ApiCaseService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用例/配置列表
        :param kwargs:
        :return:
        """
        parsed_data = CaseQuerySchema(**kwargs).dict()
        data = parse_pagination(ApiCase.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        for res in _result:
            if 'include' in res:
                res["include"] = list(map(int, res["include"].split(","))) if res["include"] else []
            if res.get("testcase", {}):
                res["testcase"] = json.loads(res["testcase"])
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> ApiCase:
        """
        更新保存测试用例/配置
        :param kwargs:
        :return:
        """
        parsed_data = CaseSaveOrUpdateSchema(**kwargs)
        case_info = ApiCase.get(parsed_data.id) if parsed_data.id else ApiCase()
        user_id = get_user_id_by_token()

        if config.EDIT_SWITCH:
            if case_info.created_by != user_id:
                raise ValueError(partner_errmsg.get(codes.CANNOT_EDIT_CREATED_BY_YOURSELF).format('用例'))
        case_info.update(**parsed_data.dict(exclude_none=True))
        return case_info

    @staticmethod
    def set_case_status(**kwargs: Any):
        """
        用例失效生效
        :param kwargs:
        :return:
        """
        ids = kwargs.get('ids', None)
        case_list = ApiCase.get_list(ids=ids).all()
        for case_info in case_list:
            case_info.case_status = 20 if case_info.case_status == 10 else 10
            case_info.save()

    @staticmethod
    def deleted(c_id: Union[int, str]):
        """
        删除测试用例
        :param c_id:
        :return:
        """
        case_info = ApiCase.get(c_id)
        case_info.delete() if case_info else ...

    @staticmethod
    def detail(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用例信息
        :param kwargs:
        :return:
        """
        c_id = kwargs.get('id', None)
        case_info = ApiCase.get(c_id)
        if not case_info:
            raise ValueError('当前用例不存在！')

        return case_info

    @staticmethod
    def run(**kwargs: Any):
        """
        运行测试用例
        :param kwargs:
        :return:
        """
        zr = ZeroRunner()
        case_info = ApiCase.get(kwargs.get("id"))
        case_info = ApiCaseHandle(**jsonable_encoder(case_info))
        test_case = TestCase(config=case_info.config, teststeps=[case_info.step])
        zr.run_testcase(test_case)
        summary = zr.get_summary()

        project_id = case_info.api_case.project_id
        module_id = case_info.api_case.module_id
        env_id = case_info.api_case.env_id
        report_info = ReportService.save_report(summary, project_id, module_id, env_id)

        return report_info

    @staticmethod
    def debug_testcase(**kwargs: Any) -> Any:
        """
        用例调试
        :param kwargs:
        :return:
        """
        zr = ZeroRunner()
        case_info = ApiCaseHandle(**kwargs)
        test_case = TestCase(config=case_info.config, teststeps=[case_info.step])
        zr.run_testcase(test_case)
        data = zr.get_summary().dict()
        return data

    @staticmethod
    def postman2case(json_body: Dict, **kwargs):
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
            parsed_data = CaseSaveOrUpdateSchema(**case).dict()
            case_info = ApiCase()
            case_info.update(**parsed_data)
        return len(coll.case_list)
