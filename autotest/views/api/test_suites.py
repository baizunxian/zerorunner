import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.test_suites import TestSuitesService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('suites', __name__, url_prefix='/api/testSuites')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def suites_list():
    """
    套件列表
    :return:
    """
    try:
        data = TestSuitesService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """
    更新保存套件
    :return:
    """
    try:
        data = TestSuitesService.save_or_update(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data.id)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除套件
    :return:
    """
    parsed_data = request.json
    s_id = parsed_data.get('id', None)
    try:
        TestSuitesService.deleted(s_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success()
    return partner_success()


@bp.route('/getSuiteInfo', methods=['POST'])
@login_verification
@json_required
def suite_info():
    """
    套件信息
    :return:
    """
    try:
        data = TestSuitesService.get_suite_info(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)
