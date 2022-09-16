import json
import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.test_case import CaseService
from autotest.tasks.test_case import async_run_case, run_timed_task
from autotest.utils.api import partner_success

bp = Blueprint('test_case', __name__, url_prefix='/api/testcase')


@bp.route('/list', methods=['POST'])
def case_list():
    """
    获取用例列表
    :return:
    """
    result = CaseService.list(**request.json)
    return partner_success(data=result)


@bp.route('/getTestCaseInfo', methods=['POST'])
def get_case_info():
    """
    获取用例信息
    :return:
    """
    case_info = CaseService.detail(**request.json)
    return partner_success(case_info)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存测试用例
    :return:
    """
    parsed_data = request.json
    case_info = CaseService.save_or_update(**parsed_data)
    return partner_success(case_info.id)


@bp.route('/setCaseStatus', methods=['POST'])
def set_case_status():
    """
    用例失效生效
    :return:
    """
    parsed_data = request.json
    CaseService.set_case_status(**parsed_data)
    return partner_success()


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除用例
    :return:
    """
    parsed_data = request.json
    c_id = parsed_data.get('id', None)
    CaseService.deleted(c_id)
    return partner_success()


@bp.route('/runTestCase', methods=['POST'])
def run_test():
    """
    运行用例
    :return:
    """
    parsed_data = request.json
    params = CaseService.run_make(**parsed_data)  # 初始化校验，避免生成用例是出错
    if parsed_data.get('run_mode', None) == 2:
        logger.info('异步执行用例 ~')
        async_run_case.delay(**params)
        return partner_success(code=codes.PARTNER_CODE_OK, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
    else:
        summary = CaseService.run(**params)
        return partner_success(data=summary)


@bp.route('/runTestCaseNew', methods=['POST'])
def run_test_new():
    """
    运行用例
    :return:
    """
    parsed_data = request.json
    params = CaseService.run_make_new(**parsed_data)  # 初始化校验，避免生成用例是出错
    if parsed_data.get('run_mode', None) == 2:
        logger.info('异步执行用例 ~')
        async_run_case.delay(**params)
        return partner_success(code=codes.PARTNER_CODE_OK, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
    else:
        summary = CaseService.run(**params)
        return partner_success(data=summary)


@bp.route('/debugTestCase', methods=['POST'])
def debug_testcase():
    """
    调试用例
    :return:
    """
    data = CaseService.debug_testcase(**request.json)
    return partner_success(data)


@bp.route('/debugTestCaseNew', methods=['POST'])
def debug_testcase_new():
    """
    调试用例
    :return:
    """
    data = CaseService.debug_testcase_new(**request.json)
    return partner_success(data)


@bp.route('/testRunCase', methods=['POST'])
def test_run_case():
    """
    测试运行用例
    :return:
    """
    data = run_timed_task(**request.json)
    return partner_success(data)


@bp.route('/postman2case', methods=['POST'])
def postman2case():
    """
    postman 文件转用例
    :return:
    """
    postman_file = request.files.get('file', None)
    if not postman_file:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择导入的postman，json文件！')
    if postman_file.filename.split('.')[-1] != 'json':
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择json文件导入！')
    json_body = json.load(postman_file)
    data = CaseService.postman2case(json_body, **request.form)
    return partner_success(data)
