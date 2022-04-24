import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.test_case import CaseService
from autotest.tasks.test_case import async_run_case
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('test_case', __name__, url_prefix='/api/testcase')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def case_list():
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
    """更新保存测试用例"""
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
    """用例失效生效"""
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
    """删除用例"""
    parsed_data = request.json
    c_id = parsed_data.get('id', None)
    try:
        CaseService.deleted(c_id)
    except Exception as err:
        logger.error(traceback.format_exc())
    return partner_success()


@bp.route('/debugTestCase', methods=['POST'])
@login_verification
@json_required
def debug_testcase():
    """debug 用例"""
    try:
        data = CaseService.debug_testcase(**request.json)
        return partner_success(data)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))


@bp.route('/runTestCase', methods=['POST'])
@login_verification
@json_required
def run_test():
    """运行用例"""
    try:
        parsed_data = request.json
        params = CaseService.run_make(**parsed_data)  # 初始化校验，避免生成用例是出错
        if parsed_data.get('run_mode', None) == 2:
            async_run_case.delay(**params)
            return partner_success(code=codes.PARTNER_CODE_OK, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
        else:
            summary = CaseService.run(**params)
            return partner_success(data=summary)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
