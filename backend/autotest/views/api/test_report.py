from flask import Blueprint, request

from autotest.services.api_services.test_report import ReportService
from autotest.utils.api import partner_success

bp = Blueprint('test_report', __name__, url_prefix='/api/report', template_folder='httprunner')


@bp.route('/list', methods=['POST'])
def report_list():
    """
    测试报告列表
    :return:
    """
    data = ReportService.list(**request.json)
    return partner_success(data=data)


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除报告
    :return:
    """
    parsed_data = request.json
    report_id = parsed_data.get('id', None)
    ReportService.deleted(report_id)
    return partner_success()


@bp.route('/getReportById', methods=['POST'])
def get_report_by_id():
    """
    测试报告
    :return:
    """
    parsed_data = request.json
    report_id = parsed_data.get('id', None)
    report_info = ReportService.detail(report_id)
    return partner_success(data=report_info)
