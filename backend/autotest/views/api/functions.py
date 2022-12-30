from flask import Blueprint, request

from autotest.exc import codes
from autotest.services.api_services.functions import FunctionsService
from autotest.utils.api import partner_success

bp = Blueprint('functions', __name__, url_prefix='/api/functions')


@bp.route('/list', methods=['POST'])
def get_debug_talk_list():
    """
    获取自定义函数列表
    :return:
    """
    result = FunctionsService.list(**request.json)
    return partner_success(data=result)


@bp.route('/getFuncInfo', methods=['POST'])
def get_debug_talk_info():
    """
    获取自定义函数详情
    :return:
    """
    data = FunctionsService.get_function_info(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_debug_talk():
    """
    更新保存
    :return:
    """
    # return partner_success(code=codes.PARTNER_CODE_FAIL, msg='演示环境不保存！')
    data = FunctionsService.save_or_update(**request.json)
    return partner_success(data=data)


@bp.route('/getFuncList', methods=['POST'])
def get_func_list():
    """
    获取函数列表
    :return:
    """
    try:
        parsed_data = request.json
        func_id = parsed_data.get('id', None)
        func_name = parsed_data.get('func_name', None)
        func_list = FunctionsService.get_function_by_id(func_id, func_name).get('func_list')
        return partner_success(data=func_list)
    except Exception as err:
        raise ValueError(f"查询函数名称失败:{err}")


@bp.route('/debugFunc', methods=['POST'])
def debug_func():
    """
    函数调试
    :return:
    """
    parsed_data = request.json
    try:
        result = FunctionsService.debug_func(**parsed_data)
        return partner_success({'result': result})
    except Exception as err:
        raise ValueError(f"执行函数失败:{err}")
