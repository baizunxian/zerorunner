import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.lookup import LookupService, LookupValueService
from autotest.utils.api import partner_success, login_verification, json_required

bp = Blueprint('lookup', __name__, url_prefix='/api/lookup')


@bp.route('/getAllLookup', methods=['POST'])
@login_verification
@json_required
def get_all_lookup():
    """
    获取所有数据字典
    :return:
    """
    try:
        data = LookupValueService.get_all_lookup()
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/getLookupList', methods=['POST'])
@login_verification
@json_required
def lookup_list():
    """
    获取数据字典列表
    :return:
    """
    try:
        data = LookupService.list(**request.json)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdateLookup', methods=['POST'])
@login_verification
@json_required
def save_or_update_lookup():
    """新增或更新字典"""
    try:
        data = LookupService.save_or_update(**request.json)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data.id)


@bp.route('/delLookup', methods=['POST'])
@login_verification
@json_required
def del_lookup():
    """删除字典"""
    try:
        parsed_data = request.json
        id = parsed_data.get('id', None)
        LookupService.deleted(id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/getLookupValue', methods=['POST'])
@login_verification
@json_required
def get_lookup_value():
    """获取字典值"""
    try:
        data = LookupValueService.get_lookup_value(**request.json)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdateLookupValue', methods=['POST'])
@login_verification
@json_required
def save_or_update_lookup_value():
    """保存或更新字典值"""
    try:
        data = LookupValueService.save_or_update(**request.json)
    except ValueError as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data.id)


@bp.route('/delLookupValue', methods=['POST'])
@login_verification
@json_required
def del_lookup_value():
    """删除字典值"""
    try:
        parsed_data = request.json
        id = parsed_data.get('id', None)
        LookupValueService.deleted(id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
