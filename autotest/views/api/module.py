import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.module import ModuleService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('module', __name__, url_prefix='/api/module')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def module_list():
    """
    模块列表
    :return:
    """
    try:
        data = ModuleService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """
    更新保存项目
    :return:
    """
    parsed_data = request.json
    try:
        data = ModuleService.save_or_update(**parsed_data)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data.id)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除模块
    :return:
    """
    try:
        parsed_data = request.json
        id = parsed_data.get('id', None)
        ModuleService.deleted(id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
