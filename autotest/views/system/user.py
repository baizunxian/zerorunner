import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.user import UserService
from autotest.utils.api import json_required, partner_success, login_verification

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/login', methods=['POST'])
@json_required
def login():
    """
    登录
    :return:
    """
    try:
        result = UserService.login(**request.json)
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(result)


@bp.route('/logout', methods=['POST'])
def logout():
    """
    登出
    :return:
    """
    UserService.logout()
    return partner_success()


@bp.route('/getUserInfoByToken', methods=['POST'])
@login_verification
@json_required
def get_user_info():
    """
    根据token获取用户信息
    :return:
    """
    parsed_data = request.json
    token = parsed_data.get('token')
    user_info = UserService.get_user_info_by_token(token)
    return partner_success(user_info)


@bp.route('/userRegister', methods=['POST'])
@json_required
def user_register():
    """
    用户注册
    :return:
    """
    try:
        UserService.user_register(**request.json)
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/changePassword', methods=['POST'])
@json_required
@login_verification
def change_password():
    """
    修改密码
    :return:
    """
    try:
        UserService.change_password(**request.json)
    except Exception as err:
        return partner_success(code=codes.USER_ID_IS_NULL, msg=str(err))
    return partner_success()


@bp.route('/list', methods=['POST'])
@json_required
@login_verification
def user_list():
    """
    查询所用用户
    :return:
    """
    try:
        data = UserService.list(**request.json)
    except ValueError as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@json_required
@login_verification
def save_or_update():
    """
    更新保存用户
    :return:
    """
    parsed_data = request.json
    try:
        UserService.save_or_update(**parsed_data)
    except ValueError as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/deleted', methods=['POST'])
@json_required
@login_verification
def deleted():
    """
    删除用户
    :return:
    """
    return partner_success(code=codes.PARTNER_CODE_FAIL, msg='限制删除用户')
    parsed_data = request.json
    id = parsed_data.get('id', None)
    UserService.deleted(id)
    return partner_success()


@bp.route('/authorizeToken', methods=['POST'])
@json_required
def authorize_token():
    parsed_data = request.json
    token = parsed_data.get('token', '')
    try:
        user_info = UserService.check_token(token)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='token已失效')
    return partner_success(user_info)
