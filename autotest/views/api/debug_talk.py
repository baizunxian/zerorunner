import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.api_services.debug_talk import DebugTalkService
from autotest.utils.api import login_verification, json_required, partner_success

bp = Blueprint('debugTalk', __name__, url_prefix='/api/debugTalk')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def get_debug_talk_list():
    """
    获取自定义函数列表
    :return:
    """
    try:
        result = DebugTalkService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=result)


@bp.route('/getDebugTalkInfo', methods=['POST'])
@login_verification
@json_required
def get_debug_talk_info():
    """
    获取自定义函数详情
    :return:
    """
    try:
        data = DebugTalkService.get_debug_talk_info(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_debug_talk():
    """
    更新保存
    :return:
    """
    try:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='演示环境不保存！')
        data = DebugTalkService.save_or_update(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
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
        func_list = DebugTalkService.get_function_by_path(func_id, func_name).get('func_list')
        return partner_success(data=func_list)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=repr(f'查询函数名称失败：{err}'))


@bp.route('/debugFunc', methods=['POST'])
def debug_func():
    """
    函数调试
    :return:
    """
    parsed_data = request.json
    try:
        result = DebugTalkService.debug_func(**parsed_data)
        return partner_success({'result': result})
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=repr(f'执行函数失败：{err}'))
