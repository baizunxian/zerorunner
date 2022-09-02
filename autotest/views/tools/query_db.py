import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.role import RolesService
from autotest.utils.api import partner_success, login_verification

bp = Blueprint('query_db', __name__, url_prefix='/api/queryDB')


@bp.route('/DBList', methods=['POST'])
def all_roles():
    """
    获取所有角色数据
    :return:
    """
    try:
        data = RolesService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)
