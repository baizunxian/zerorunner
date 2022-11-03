from flask import Blueprint, request

from autotest.services.sys_services.role import RolesService
from autotest.utils.api import partner_success

bp = Blueprint('roles', __name__, url_prefix='/api/roles')


@bp.route('/list', methods=['POST'])
def all_roles():
    """
    获取所有角色数据
    :return:
    """
    data = RolesService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    新增或更新角色
    :return:
    """
    RolesService.save_or_update(**request.json)
    return partner_success()


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除角色
    :return:
    """
    parsed_data = request.json
    r_id = parsed_data.get('id', None)
    RolesService.deleted(r_id)
    return partner_success()
