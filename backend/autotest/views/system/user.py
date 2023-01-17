from flask import Blueprint, request

from autotest.exc import codes
from autotest.services.sys_services.user import UserService
from autotest.utils.api import partner_success

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/login', methods=['POST'])
def login():
    """
    登录-
    :return:
    """
    result = UserService.login(**request.json)
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
def get_user_info():
    """
    根据token获取用户信息
    :return:
    """
    token = request.headers.get("token")
    user_info = UserService.get_user_info_by_token(token)
    return partner_success(user_info)


@bp.route('/userRegister', methods=['POST'])
def user_register():
    """
    用户注册
    :return:
    """
    UserService.user_register(**request.json)
    return partner_success()


@bp.route('/changePassword', methods=['POST'])
def change_password():
    """
    修改密码
    :return:
    """
    UserService.change_password(**request.json)
    return partner_success()


@bp.route('/list', methods=['POST'])
def user_list():
    """
    查询所用用户
    :return:
    """
    data = UserService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存用户
    :return:
    """
    parsed_data = request.json
    data = UserService.save_or_update(**parsed_data)
    return partner_success(data)


@bp.route('/deleted', methods=['POST'])
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
def authorize_token():
    parsed_data = request.json
    token = parsed_data.get('token', '')
    user_info = UserService.check_token(token)
    return partner_success(user_info)


@bp.route('/getMenuByToken', methods=['POST'])
def get_menu_by_token():
    user_info = UserService.get_menu_by_token()
    return partner_success(user_info)
