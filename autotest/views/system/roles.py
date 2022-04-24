import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.role import RolesService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('roles', __name__, url_prefix='/api/roles')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
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


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """
    新增或更新角色
    :return:
    """
    try:
        RolesService.save_or_update(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除角色
    :return:
    """
    parsed_data = request.json
    r_id = parsed_data.get('id', None)
    try:
        RolesService.deleted(r_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
