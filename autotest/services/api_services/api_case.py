import copy
import json
import os
import shutil
import traceback
import uuid
from typing import Dict, Any, List, Union, Text

import pytest
from loguru import logger

from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.httprunner.initialize_not_yaml import TestCaseMateNew
from autotest.models.api_models import ApiCase, ApiSuite, ModuleInfo
from autotest.serialize.api_serializes.api_case import (CaseQuerySchema, CaseSaveOrUpdateSchema,
                                                        TestCaseRunSchema, TestCaseRunBodySchema,
                                                        TestCaseRunBatchSchema)
from autotest.services.api_services.run_handle import ApiCaseHandle
from autotest.services.api_services.test_report import ReportService
from autotest.services.utils_services.postman2case import Collection
from autotest.utils.api import parse_pagination, jsonable_encoder
from autotest.utils.common import get_user_id_by_token, get_timestamp
from autotest.utils.service_utils import DumpTestCase
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
        case_info.update(**parsed_data.dict())
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
    def run_make(**kwargs: Any):
        """
        执行测试用例
        :param kwargs:
        :return:
        """
        zr = ZeroRunner()
        case_info = ApiCaseHandle(**kwargs)
        test_case = TestCase(config=case_info.config, teststeps=[case_info.step])
        zr.run_testcase(test_case)
        print(zr.get_summary())
        #
        # run_type_data = ApiCaseService.handle_run_type(**kwargs)
        # testcase_dir_path = run_type_data.get('testcase_dir_path', None)
        # test_path_set = TestCaseMate().main_make([testcase_dir_path])
        # params = dict(test_path_set=test_path_set, run_type_data=run_type_data)
        # logger.info('用例初始化完成~')
        return zr.get_summary()


    @staticmethod
    def run_make_new(**kwargs: Any) -> Dict[Text, Any]:
        """
        执行测试用例
        :param kwargs:
        :return:
        """
        base_url = kwargs.get('base_url', '')
        test_mate = TestCaseMateNew(base_url)
        run_type_data = ApiCaseService.handle_run_type_new(test_mate, **kwargs)
        test_path_set = test_mate.get_test_path_set()
        params = dict(test_path_set=test_path_set, run_type_data=run_type_data)
        logger.info('用例初始化完成~')
        return params

    @staticmethod
    def run(test_path_set: List[Text], run_type_data: Dict) -> Dict[Text, Any]:
        """
        运行用例
        :param test_path_set: py用例列表
        :param run_type_data: 组装数据
        :return:
        """
        testcase_dir_path = run_type_data['testcase_dir_path']  # 用例目录地址
        try:
            extra_args = ['-vs', '-W', 'ignore:Module already imported:pytest.PytestWarning']
            extra_args.extend(test_path_set)
            logger.info('执行用例 ~')
            pytest.main(extra_args)
            summary_path = run_type_data['summary_path']
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                ApiCaseService.handle_report_summary(summary=summary, run_type_data=run_type_data)
                return summary
            raise ValueError('测试用例执行失败，未获取到测试报告！')
        except Exception as err:
            logger.error(traceback.format_exc())
        finally:
            shutil.rmtree(testcase_dir_path)

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
    def handle_report_summary(summary: Dict, run_type_data: Dict):
        """
        处理报告并入库
        :param summary:
        :param run_type_data:
        :return:
        """
        test_report = ReportService.make_report(summary)
        test_report.update(run_type_data)
        ReportService.save_report(**test_report)

    @staticmethod
    def get_testcase_dir_path() -> Text:
        """
        生成用例运行地址
        :return:
        """
        return os.path.join(config.TEST_DIR, f'run_test_{get_timestamp()}')

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