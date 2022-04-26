import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.env import EnvService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('env', __name__, url_prefix='/api/env')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def env_list():
    """
    获取列表
    :return:
    """
    try:
        data = EnvService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update_env():
    """
    更新保存环境信息
    :return:
    """
    try:
        data = EnvService.save_or_update(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data.id)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def delete_env():
    """
    删除环境
    :return:
    """
    try:
        parsed_data = request.json
        env_id = parsed_data.get('id', None)
        EnvService.deleted(env_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
