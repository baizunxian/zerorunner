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
from autotest.httprunner.initialize import TestCaseMate
from autotest.httprunner.initialize_not_yaml import TestCaseMateNew
from autotest.models.api_models import CaseInfo, TestSuite, ModuleInfo
from autotest.serialize.api_serializes.test_case import (CaseQuerySchema, CaseInfoListSchema, CaseSaveOrUpdateSchema,
                                                         TestCaseRunSchema, TestCaseRunBodySchema,
                                                         TestCaseRunBatchSchema)
from autotest.services.api_services.test_report import ReportService
from autotest.services.utils_services.postman2case import Collection
from autotest.utils.api import parse_pagination
from autotest.utils.common import get_user_id_by_token, get_timestamp
from autotest.utils.service_utils import DumpTestCase


class CaseService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用例/配置列表
        :param kwargs:
        :return:
        """
        parsed_data = CaseQuerySchema().load(kwargs)
        data = parse_pagination(CaseInfo.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': CaseInfoListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> CaseInfo:
        """
        更新保存测试用例/配置
        :param kwargs:
        :return:
        """
        parsed_data = CaseSaveOrUpdateSchema().load(kwargs)
        # case_data = make_testcase(**case_data)
        case_id = parsed_data.get('id', None)
        case_info = CaseInfo.get(case_id) if case_id else CaseInfo()
        user_id = get_user_id_by_token()

        if config.EDIT_SWITCH:
            if case_info.created_by != user_id:
                raise ValueError(partner_errmsg.get(codes.CANNOT_EDIT_CREATED_BY_YOURSELF).format('用例'))
        case_info.update(**parsed_data)
        return case_info

    @staticmethod
    def set_case_status(**kwargs: Any):
        """
        用例失效生效
        :param kwargs:
        :return:
        """
        ids = kwargs.get('ids', None)
        for case_id in ids:
            case_info = CaseInfo.get(case_id)
            if case_info:
                case_info.case_status = 20 if case_info.case_status == 10 else 10
                case_info.save()

    @staticmethod
    def deleted(c_id: Union[int, str]):
        """
        删除测试用例
        :param c_id:
        :return:
        """
        case_info = CaseInfo.get(c_id)
        case_info.delete() if case_info else ...

    @staticmethod
    def get_testcase_info(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用例信息
        :param kwargs:
        :return:
        """
        c_id = kwargs.get('id', None)
        case_info = CaseInfo.get(c_id)
        if not case_info:
            raise ValueError('当前用例不存在！')
        case_info = CaseInfoListSchema().dump(case_info)
        return case_info

    @staticmethod
    def run_make(**kwargs: Any) -> Dict[Text, Any]:
        """
        执行测试用例
        :param kwargs:
        :return:
        """
        run_type_data = CaseService.handle_run_type(**kwargs)
        testcase_dir_path = run_type_data.get('testcase_dir_path', None)
        test_path_set = TestCaseMate().main_make([testcase_dir_path])
        params = dict(test_path_set=test_path_set, run_type_data=run_type_data)
        logger.info('用例初始化完成~')
        return params

    @staticmethod
    def run_make_new(**kwargs: Any) -> Dict[Text, Any]:
        """
        执行测试用例
        :param kwargs:
        :return:
        """
        base_url = kwargs.get('base_url', '')
        test_mate = TestCaseMateNew(base_url)
        run_type_data = CaseService.handle_run_type_new(test_mate, **kwargs)
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
                CaseService.handle_report_summary(summary=summary, run_type_data=run_type_data)
                return summary
            raise ValueError('测试用例执行失败，未获取到测试报告！')
        except Exception as err:
            logger.error(traceback.format_exc())
        finally:
            shutil.rmtree(testcase_dir_path)

    @staticmethod
    def debug_testcase(**kwargs: Any) -> Dict[Text, Any]:
        """
        用例调试
        :param kwargs:
        :return:
        """
        testcase_dir_path = CaseService.get_testcase_dir_path()
        case_hex = f'test_case{uuid.uuid4().hex[:6]}'
        debug_data = {
            'case_info': kwargs,
            'base_url': kwargs.get('base_url', None),
            'testcase_dir_path': testcase_dir_path,
            'case_hex': case_hex
        }
        DumpTestCase(**debug_data)
        summary_path = os.path.join(testcase_dir_path, case_hex, 'summary.json')
        test_path_set = TestCaseMate().main_make([testcase_dir_path])
        extra_args_new = ['-vs', '-W', 'ignore:Module already imported:pytest.PytestWarning']
        extra_args_new.extend(test_path_set)
        try:
            pytest.main(extra_args_new)
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                return summary
            return {}
        except Exception as err:
            logger.error(traceback.format_exc())
        finally:
            shutil.rmtree(testcase_dir_path)
            # ...

    @staticmethod
    def debug_testcase_new(**kwargs: Any) -> Dict[Text, Any]:
        """
        用例调试
        :param kwargs:
        :return:
        """
        case_mate = TestCaseMateNew(kwargs.get('base_url', ''))
        case_mate.debug_case_make(kwargs)

        summary_path = case_mate.summary_path
        extra_args_new = ['-vs', '-W', 'ignore:Module already imported:pytest.PytestWarning']
        extra_args_new.extend(case_mate.get_test_path_set())
        try:
            pytest.main(extra_args_new)
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                return summary
            return {}
        except Exception as err:
            logger.error(traceback.format_exc())
        finally:
            shutil.rmtree(case_mate.testcase_dir_path)
            # ...

    @staticmethod
    def handle_run_type(**kwargs: Any) -> Dict[Text, Any]:
        """
        不同模式运行处理
        module 模块
        suite 套件
        case 用例
        :param kwargs:
        :return:
        """
        parsed_data = TestCaseRunSchema().load(kwargs)
        # run_type 运行类型 模块，套件，用例
        id = parsed_data.get('id', None)
        run_type = parsed_data.pop('run_type', None)
        base_url = parsed_data.get('base_url', None)
        testcase_dir_path = CaseService.get_testcase_dir_path()
        number_of_run = parsed_data.get('number_of_run', None)
        case_hex = f'testcase_{uuid.uuid4().hex[:6]}'
        data = {
            'name': '',
            'summary_path': os.path.join(testcase_dir_path, case_hex, 'summary.json'),
            'project_id': None,
            'module_id': None,
            'execute_user_id': get_user_id_by_token(),
            'run_type': run_type,
            'run_mode': parsed_data.get('run_mode', None),
            'testcase_dir_path': testcase_dir_path,
        }

        if run_type == 'module':
            module_info = ModuleInfo.get(id)

            if not module_info:
                raise ValueError('当前模块没有关联用例')
            data['name'] = module_info.name
            data['project_id'] = module_info.project_id
            data['module_id'] = module_info.id
            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_module_id(module_id=id, case_type=1).all(),
                                                     many=True)
            for case in case_list:
                run_parsed_data = dict(
                    case_info=case,
                    base_url=base_url,
                    testcase_dir_path=testcase_dir_path,
                    number_of_run=number_of_run,
                    case_hex=case_hex,
                )
                DumpTestCase(**run_parsed_data)

        elif run_type == 'suite':
            suite_info = TestSuite.get(id)
            if not suite_info:
                raise ValueError('套件没有关联用例！')
            data['name'] = suite_info.name
            data['project_id'] = suite_info.project_id
            data['module_id'] = None
            ids = suite_info.include.split(',')
            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_ids(ids=ids, case_type=1).all(),
                                                     many=True)
            for case in case_list:
                run_parsed_data = dict(
                    case_info=case,
                    base_url=base_url,
                    testcase_dir_path=testcase_dir_path,
                    number_of_run=number_of_run,
                    case_hex=case_hex,
                )
                DumpTestCase(**run_parsed_data)
        else:
            case_info = CaseInfo.get(id)
            if not case_info:
                raise ValueError('当前用例不存在！')
            data['name'] = case_info.name
            data['project_id'] = case_info.project_id
            data['module_id'] = case_info.module_id
            case_info = TestCaseRunBodySchema().dump(case_info)
            run_parsed_data = dict(
                case_info=case_info,
                base_url=base_url,
                testcase_dir_path=testcase_dir_path,
                number_of_run=number_of_run,
                case_hex=case_hex,
            )
            DumpTestCase(**run_parsed_data)
        return data

    @staticmethod
    def handle_run_type_new(test_mate: "TestCaseMateNew", **kwargs: Any) -> Dict[Text, Any]:
        """
        不同模式运行处理
        module 模块
        suite 套件
        case 用例
        :param test_mate: TestCaseMateNew 对象
        :param kwargs:
        :return:
        """
        parsed_data = TestCaseRunSchema().load(kwargs)
        user_id = get_user_id_by_token()
        # run_type 运行类型 模块，套件，用例
        id = parsed_data.get('id', None)
        run_type = parsed_data.pop('run_type', None)
        run_mode = parsed_data.pop('run_mode', None)

        test_mate.run_type = run_type
        test_mate.run_mode = run_mode
        test_mate.execute_user_id = user_id

        if run_type == 'module':
            module_info = ModuleInfo.get(id)

            if not module_info:
                raise ValueError('当前模块没有关联用例')

            test_mate.name = module_info.name
            test_mate.project_id = module_info.project_id
            test_mate.module_id = module_info.module_id

            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_module_id(module_id=id, case_type=1).all(),
                                                     many=True)
            test_mate.run_case_make(case_list)

        elif run_type == 'suite':
            suite_info = TestSuite.get(id)
            if not suite_info:
                raise ValueError('套件没有关联用例！')
            test_mate.name = suite_info.name
            test_mate.project_id = suite_info.project_id
            test_mate.module_id = None
            ids = suite_info.include.split(',')
            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_ids(ids=ids, case_type=1).all(),
                                                     many=True)
            test_mate.run_case_make(case_list)

        else:
            case_info = CaseInfo.get(id)
            if not case_info:
                raise ValueError('当前用例不存在！')
            test_mate.name = case_info.name
            test_mate.project_id = case_info.project_id
            test_mate.module_id = case_info.module_id
            case_info = TestCaseRunBodySchema().dump(case_info)
            test_mate.run_case_make([case_info])

        data = {
            'name': test_mate.name,
            'summary_path': test_mate.summary_path,
            'project_id': test_mate.project_id,
            'module_id': test_mate.module_id,
            'execute_user_id': test_mate.execute_user_id,
            'run_type': test_mate.run_type,
            'run_mode': test_mate.run_mode,
            'testcase_dir_path': test_mate.testcase_dir_path,
        }
        return data

    @staticmethod
    def handle_run_type_batch(test_mate: "TestCaseMateNew", **kwargs: Any) -> Dict[Text, Any]:
        """
        批量运行
        module 模块
        suite 套件
        case 用例
        :param test_mate: TestCaseMateNew 对象
        :param kwargs:
        :return:
        """
        parsed_data = TestCaseRunBatchSchema().load(kwargs)
        ids = parsed_data.get('ids', None)
        user_id = parsed_data.pop('ex_user_id', None)
        run_type = parsed_data.pop('run_type', None)
        project_id = parsed_data.pop('project_id', None)
        run_mode = parsed_data.pop('run_mode', None)
        name = parsed_data.pop('name', None)

        test_mate.name = name
        test_mate.run_type = run_type
        test_mate.run_mode = run_mode
        test_mate.execute_user_id = user_id
        test_mate.project_id = project_id

        if run_type == 'module':

            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_module_id(module_ids=ids, case_type=1).all(),
                                                     many=True)
            test_mate.run_case_make(case_list)

        elif run_type == 'suite':
            suite_list = TestSuite.get_list(ids=ids).all()
            case_ids = set()
            for suite in suite_list:
                includes = set(map(int, (suite.include.split(','))))
                case_ids = case_ids.union(includes)
            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_ids(ids=case_ids, case_type=1).all(),
                                                     many=True)
            test_mate.run_case_make(case_list)

        else:
            case_list = TestCaseRunBodySchema().dump(CaseInfo.get_case_by_ids(ids=ids), many=True)
            test_mate.run_case_make(case_list)

        data = {
            'name': test_mate.name,
            'summary_path': test_mate.summary_path,
            'project_id': test_mate.project_id,
            'module_id': test_mate.module_id,
            'execute_user_id': test_mate.execute_user_id,
            'run_type': test_mate.run_type,
            'run_mode': test_mate.run_mode,
            'testcase_dir_path': test_mate.testcase_dir_path,
        }
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
            parsed_data = CaseSaveOrUpdateSchema().load(case)
            case_info = CaseInfo()
            case_info.update(**parsed_data)
        return len(coll.case_list)
