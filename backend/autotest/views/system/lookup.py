from flask import Blueprint, request

from autotest.services.sys_services.lookup import LookupService, LookupValueService
from autotest.utils.api import partner_success

bp = Blueprint('lookup', __name__, url_prefix='/api/lookup')


@bp.route('/getAllLookup', methods=['POST'])
def get_all_lookup():
    """
    获取所有数据字典
    :return:
    """
    data = LookupValueService.get_all_lookup()
    return partner_success(data=data)


@bp.route('/getLookupList', methods=['POST'])
def lookup_list():
    """
    获取数据字典列表
    :return:
    """
    data = LookupService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdateLookup', methods=['POST'])
def save_or_update_lookup():
    """新增或更新字典"""
    data = LookupService.save_or_update(**request.json)
    return partner_success(data.id)


@bp.route('/delLookup', methods=['POST'])
def del_lookup():
    """删除字典"""
    parsed_data = request.json
    id = parsed_data.get('id', None)
    LookupService.deleted(id)
    return partner_success()


@bp.route('/getLookupValue', methods=['POST'])
def get_lookup_value():
    """获取字典值"""
    data = LookupValueService.get_lookup_value(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdateLookupValue', methods=['POST'])
def save_or_update_lookup_value():
    """保存或更新字典值"""
    data = LookupValueService.save_or_update(**request.json)
    return partner_success(data.id)


@bp.route('/delLookupValue', methods=['POST'])
def del_lookup_value():
    """删除字典值"""
    parsed_data = request.json
    id = parsed_data.get('id', None)
    LookupValueService.deleted(id)
    return partner_success()
