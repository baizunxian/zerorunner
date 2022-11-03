from flask import Blueprint, request

from autotest.services.sys_services.role import RolesService
from autotest.utils.api import partner_success

bp = Blueprint('query_db', __name__, url_prefix='/api/queryDB')


@bp.route('/DBList', methods=['POST'])
def all_roles():
    """
    获取所有角色数据
    :return:
    """
    data = RolesService.list(**request.json)
    return partner_success(data=data)
