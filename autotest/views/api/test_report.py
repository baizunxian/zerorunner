import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.test_report import ReportService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('test_report', __name__, url_prefix='/api/report', template_folder='httprunner')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def report_list():
    """
    测试报告列表
    :return:
    """
    try:
        data = ReportService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除报告
    :return:
    """
    parsed_data = request.json
    try:
        report_id = parsed_data.get('id', None)
        ReportService.deleted(report_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success()
    return partner_success()


@bp.route('/getReportById', methods=['POST'])
@login_verification
@json_required
def get_report_by_id():
    """
    测试报告
    :return:
    """
    parsed_data = request.json
    try:
        report_id = parsed_data.get('id', None)
        report_info = ReportService.get_report_by_id(report_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=report_info)
