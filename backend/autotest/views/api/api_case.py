from flask import Blueprint, request

from autotest.services.api_services.api_case import ApiCaseService
from autotest.utils.api import partner_success

bp = Blueprint('api_case', __name__, url_prefix='/api/apiCase')


@bp.route('/list', methods=['POST'])
def suites_list():
    """
    套件列表
    :return:
    """
    data = ApiCaseService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存套件
    :return:
    """
    data = ApiCaseService.save_or_update(**request.json)
    return partner_success(data=data.id)


@bp.route('/runTestCase', methods=['POST'])
def run_testcase():
    """
    运行用例
    :return:
    """
    data = ApiCaseService.run_case(**request.json)
    return partner_success(data)


@bp.route('/debugTestCase', methods=['POST'])
def debug_testcase():
    """
    调试用例
    :return:
    """
    data = ApiCaseService.debug_case(**request.json)
    return partner_success(data=data)


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除套件
    :return:
    """
    parsed_data = request.json
    s_id = parsed_data.get('id', None)
    ApiCaseService.deleted(s_id)
    return partner_success()


@bp.route('/getSuiteInfo', methods=['POST'])
def suite_info():
    """
    套件信息
    :return:
    """
    data = ApiCaseService.get_case_info(**request.json)
    return partner_success(data=data)
