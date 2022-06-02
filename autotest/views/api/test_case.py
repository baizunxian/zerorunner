import json
import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.test_case import CaseService
from autotest.tasks.test_case import async_run_case, run_timed_task
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('test_case', __name__, url_prefix='/api/testcase')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def case_list():
    """
    获取用例列表
    :return:
    """
    try:
        result = CaseService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=result)


@bp.route('/getTestCaseInfo', methods=['POST'])
@login_verification
@json_required
def get_case_info():
    """
    获取用例信息
    :return:
    """
    try:
        case_info = CaseService.get_testcase_info(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(case_info)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """
    更新保存测试用例
    :return:
    """
    parsed_data = request.json
    try:
        case_info = CaseService.save_or_update(**parsed_data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(case_info.id)


@bp.route('/setCaseStatus', methods=['POST'])
@login_verification
@json_required
def set_case_status():
    """
    用例失效生效
    :return:
    """
    try:
        parsed_data = request.json
        CaseService.set_case_status(**parsed_data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除用例
    :return:
    """
    parsed_data = request.json
    c_id = parsed_data.get('id', None)
    try:
        CaseService.deleted(c_id)
    except Exception as err:
        logger.error(traceback.format_exc())
    return partner_success()


@bp.route('/runTestCase', methods=['POST'])
@login_verification
@json_required
def run_test():
    """
    运行用例
    :return:
    """
    try:
        parsed_data = request.json
        params = CaseService.run_make(**parsed_data)  # 初始化校验，避免生成用例是出错
        if parsed_data.get('run_mode', None) == 2:
            logger.info('异步执行用例 ~')
            async_run_case.delay(**params)
            return partner_success(code=codes.PARTNER_CODE_OK, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
        else:
            summary = CaseService.run(**params)
            return partner_success(data=summary)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/runTestCaseNew', methods=['POST'])
@login_verification
@json_required
def run_test_new():
    """
    运行用例
    :return:
    """
    try:
        parsed_data = request.json
        params = CaseService.run_make_new(**parsed_data)  # 初始化校验，避免生成用例是出错
        if parsed_data.get('run_mode', None) == 2:
            logger.info('异步执行用例 ~')
            async_run_case.delay(**params)
            return partner_success(code=codes.PARTNER_CODE_OK, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
        else:
            summary = CaseService.run(**params)
            return partner_success(data=summary)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/debugTestCase', methods=['POST'])
@login_verification
@json_required
def debug_testcase():
    """
    调试用例
    :return:
    """
    try:
        data = CaseService.debug_testcase(**request.json)
        return partner_success(data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/debugTestCaseNew', methods=['POST'])
@login_verification
@json_required
def debug_testcase_new():
    """
    调试用例
    :return:
    """
    try:
        data = CaseService.debug_testcase_new(**request.json)
        return partner_success(data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/testRunCase', methods=['POST'])
@login_verification
@json_required
def test_run_case():
    """
    测试运行用例
    :return:
    """
    try:
        data = run_timed_task(**request.json)
        return partner_success(data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/postman2case', methods=['POST'])
@login_verification
def postman2case():
    """
    postman 文件转用例
    :return:
    """
    try:
        postman_file = request.files.get('file', None)
        if not postman_file:
            return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择导入的postman，json文件！')
        if postman_file.filename.split('.')[-1] != 'json':
            return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择json文件导入！')
        json_body = json.load(postman_file)
        data = CaseService.postman2case(json_body, **request.form)
        return partner_success(data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))