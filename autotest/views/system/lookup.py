from autotest.forms.form import LookupSchema, LookupValueSchema, \
    DelLookupCheckSchema
from flask import Blueprint, request
from marshmallow import ValidationError

from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.models.sys_models import Lookup, LookupValue
from autotest.utils import logger
from autotest.utils.api import partner_success, login_verification, parse_pagination, user_roles

bp = Blueprint('lookup', __name__, url_prefix='/api')


@bp.route('/lookupList', methods=['POST'])
@login_verification
def lookup_list():
    """
    获取数据字典列表
    :return:
    """
    parsed_data = request.json
    code = parsed_data.get('code', None)
    data = parse_pagination(Lookup.get_lookup_list(code))
    _result, pagination = data.get('result'), data.get('pagination')
    _result = LookupSchema().dump(_result, many=True)
    result = {
        'rows': _result
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/saveOrUpdateLookup', methods=['POST'])
@login_verification
@user_roles(id_type='lookup')
def save_or_update_lookup():
    """新增或更新字典"""
    parsed_data = request.json
    id = parsed_data.get('id', None)
    code = parsed_data.get('code', None)
    description = parsed_data.get('description', None)
    created_by = parsed_data.get('user_id', None)
    if id:
        lookup = Lookup.get(id)
        if code != lookup.code:
            if Lookup.get_lookup_list(code).count():
                return partner_success(code=codes.PARTNER_CODE_FAIL, msg='编码已存在！')
    else:
        if Lookup.get_lookup_list(code).count():
            return partner_success(code=codes.PARTNER_CODE_FAIL, msg='编码已存在！')
        lookup = Lookup()
        lookup.created_by = created_by
    lookup.code = code
    lookup.description = description
    lookup.save()
    return partner_success()


@bp.route('/delLookup', methods=['POST'])
@login_verification
@user_roles(id_type='lookup')
def del_lookup():
    """删除字典"""
    try:
        parsed_data = DelLookupCheckSchema().load(request.json)
    except ValidationError as err:
        logger.error(err.messages)
        return partner_success(
            code=codes.PARTNER_CODE_PARAMS_FAIL,
            msg=partner_errmsg.get(codes.PARTNER_CODE_PARAMS_FAIL),
            data=err.messages,
        )
    id = parsed_data.get('id', None)
    try:
        if LookupValue.get_lookup_value_by_lookup_id(id).count():
            return partner_success(code=codes.PARTNER_CODE_FAIL, msg='数据字典类型不能直接删除，请先解除数据字典类型与数据字典关联')
        Lookup.get(id).delete()
        return partner_success()
    except Exception as err:
        logger.error(err)
        return partner_success()


@bp.route('/getLookupValue', methods=['POST'])
@login_verification
def get_lookup_value():
    """获取字典值"""
    parsed_data = request.json
    code = parsed_data.get('code', None)
    lookup_id = parsed_data.get('lookup_id', None)
    lookup_value = LookupValue.get_lookup_value(code, lookup_id)
    if lookup_value:
        lookup_value = LookupValueSchema().dump(lookup_value, many=True)
        return partner_success(lookup_value)
    return partner_success([])


@bp.route('/saveOrUpdateLookupValue', methods=['POST'])
@user_roles(id_type='lookup')
@login_verification
def save_or_update_lookup_value():
    """保存或更新字典值"""
    parsed_data = request.json
    id = parsed_data.get('id', None)
    lookup_id = parsed_data.get('lookup_id', None)
    lookup_code = parsed_data.get('lookup_code', None)
    lookup_value = parsed_data.get('lookup_value', None)
    display_sequence = parsed_data.get('display_sequence', None)
    ext = parsed_data.get('ext', None)
    created_by = parsed_data.get('user_id', None)
    if id:
        lookup_info = LookupValue.get(id)
    else:
        lookup_info = LookupValue()
    lookup_info.created_by = created_by
    lookup_info.display_sequence = display_sequence
    lookup_info.lookup_value = lookup_value
    lookup_info.lookup_code = lookup_code
    lookup_info.lookup_id = lookup_id
    lookup_info.ext = ext
    lookup_info.save()
    return partner_success()


@bp.route('/delLookupValue', methods=['POST'])
@user_roles(id_type='lookup')
@login_verification
def del_lookup_vlaue():
    """删除字典值"""
    try:
        parsed_data = DelLookupCheckSchema().load(request.json)
    except ValidationError as err:
        logger.error(err.messages)
        return partner_success(
            code=codes.PARTNER_CODE_PARAMS_FAIL,
            msg=partner_errmsg.get(codes.PARTNER_CODE_PARAMS_FAIL),
            data=err.messages,
        )
    id = parsed_data.get('id', None)
    try:
        LookupValue.get(id).delete()
        return partner_success()
    except Exception as err:
        logger.error(err)
        return partner_success()
