from flask import Blueprint, request

from autotest.services.api_services.module import ModuleService
from autotest.utils.api import partner_success

bp = Blueprint('module', __name__, url_prefix='/api/module')


@bp.route('/list', methods=['POST'])
def module_list():
    """
    模块列表
    :return:
    """
    data = ModuleService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存项目
    :return:
    """
    parsed_data = request.json
    data = ModuleService.save_or_update(**parsed_data)
    return partner_success(data.id)


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除模块
    :return:
    """
    parsed_data = request.json
    id = parsed_data.get('id', None)
    ModuleService.deleted(id)
    return partner_success()
