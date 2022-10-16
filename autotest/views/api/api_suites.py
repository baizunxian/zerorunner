from flask import Blueprint, request

from autotest.services.api_services.api_suites import ApiSuitesService
from autotest.utils.api import partner_success

bp = Blueprint('api_suites', __name__, url_prefix='/api/apiSuites')


@bp.route('/list', methods=['POST'])
def suites_list():
    """
    套件列表
    :return:
    """
    data = ApiSuitesService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存套件
    :return:
    """
    data = ApiSuitesService.save_or_update(**request.json)
    return partner_success(data=data.id)


@bp.route('/runSuites', methods=['POST'])
def run_suites():
    """
    运行套件
    :return:
    """
    data = ApiSuitesService.run_suites(**request.json)
    return partner_success(data=data.id)


@bp.route('/debugSuites', methods=['POST'])
def debug_suites():
    """
    运行套件
    :return:
    """
    data = ApiSuitesService.debug_suites(**request.json)
    return partner_success(data=data)


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除套件
    :return:
    """
    parsed_data = request.json
    s_id = parsed_data.get('id', None)
    ApiSuitesService.deleted(s_id)
    return partner_success()


@bp.route('/getSuiteInfo', methods=['POST'])
def suite_info():
    """
    套件信息
    :return:
    """
    data = ApiSuitesService.get_suite_info(**request.json)
    return partner_success(data=data)
