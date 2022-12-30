import json
import unittest
from typing import Dict, Any, Union, Text

from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.models.api_models import ApiInfo
from autotest.serialize.api_serializes.api_info import (ApiInfoQuerySchema, ApiInfoSaveOrUpdateSchema)
from autotest.services.api_services.run_handle import ApiInfoHandle
from autotest.services.utils_services.postman2case import Collection
from autotest.utils.api import parse_pagination, jsonable_encoder
from autotest.utils.common import get_user_id_by_token
from zerorunner.models import TestSuite as ZTestSuite, TestCase as ZTestCase
from zerorunner.report import HtmlTestResult
from zerorunner.runner import Runner
from zerorunner.testcase import TestCase, ZeroRunner


class ApiInfoService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        接口列表
        :param kwargs:
        :return:
        """
        parsed_data = ApiInfoQuerySchema(**kwargs).dict()
        data = parse_pagination(ApiInfo.get_list(**parsed_data))
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
    def save_or_update(**kwargs: Any) -> ApiInfo:
        """
        更新保存测试用例/配置
        :param kwargs:
        :return:
        """
        parsed_data = ApiInfoSaveOrUpdateSchema(**kwargs)
        case_info = ApiInfo.get(parsed_data.id) if parsed_data.id else ApiInfo()
        user_id = get_user_id_by_token()

        if config.EDIT_SWITCH:
            if case_info.created_by != user_id:
                raise ValueError(partner_errmsg.get(codes.CANNOT_EDIT_CREATED_BY_YOURSELF).format('用例'))
        case_info.update(**parsed_data.dict(exclude_none=True))
        return case_info

    @staticmethod
    def set_api_status(**kwargs: Any):
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
    def deleted(c_id: Union[int, str]):
        """
        删除测试用例
        :param c_id:
        :return:
        """
        case_info = ApiInfo.get(c_id)
        case_info.delete() if case_info else ...

    @staticmethod
    def detail(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用例信息
        :param kwargs:
        :return:
        """
        case_id = kwargs.get('id', None)
        case_info = ApiInfo.get_api_by_id(id=case_id)
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
        zr = Runner()
        case_info = ApiInfo.get(kwargs.get("id"))
        case_info = ApiInfoHandle(**jsonable_encoder(case_info))
        # zr.config = case_info.config
        # zr.teststeps = [case_info.step]
        # zr.run()
        # summary = zr.get_summary()
        test_case = TestCase(case_info.get_testcase())
        runner = unittest.TextTestRunner(failfast=False)
        result = runner.run(test_case)

        project_id = case_info.api_info.project_id
        module_id = case_info.api_info.module_id
        env_id = case_info.api_info.env_id
        # report_info = ReportService.save_report(summary, project_id, module_id, env_id)

        return None

    @staticmethod
    def debug_testcase(**kwargs: Any) -> Any:
        """
        用例调试
        :param kwargs:
        :return:
        """
        case_info = ApiInfoHandle(**kwargs)
        runner = ZeroRunner()
        runner.run_tests(case_info.get_testcase())
        test_case = TestCase(case_info.get_testcase())
        result = runner.run(test_case)
        return result.summary

    @staticmethod
    def postman2api(json_body: Dict, **kwargs):
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
            parsed_data = ApiInfoSaveOrUpdateSchema(**case).dict()
            case_info = ApiInfo()
            case_info.update(**parsed_data)
        return len(coll.case_list)
