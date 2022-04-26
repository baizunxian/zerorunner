import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.config import config
from autotest.exc import codes
from autotest.services.api_services.project import ProjectService
from autotest.utils.api import partner_success, login_verification, json_required

bp = Blueprint('project', __name__, url_prefix='/api/project')
auth = config.Authentication


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def project_list():
    """
    项目列表
    :return:
    """
    try:
        data = ProjectService.list(**request.json)
    except ValueError as err:
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
    try:
        data = ProjectService.save_or_update(**request.json)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data.id)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted():
    """
    删除
    :return:
    """
    try:
        parsed_data = request.json
        id = parsed_data.get('id', None)
        ProjectService.deleted(id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
