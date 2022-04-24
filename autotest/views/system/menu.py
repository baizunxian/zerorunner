import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.menu import MenuService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('menu', __name__, url_prefix='/api/menu')


@bp.route('/allMenu', methods=['POST'])
@login_verification
def all_menu():
    """
    获取所有菜单数据
    :return:
    """
    try:
        data = MenuService.all_menu()
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/getAllMenus', methods=['POST'])
@login_verification
def get_all_menus():
    """
    获取结构菜单，父子关系
    :return:
    """
    try:
        data = MenuService.all_menu_nesting()
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """
    新增或者更新menu
    :return:
    """
    try:
        MenuService.save_or_update(**request.json)
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def delete_menu():
    """
    删除菜单
    :return:
    """
    try:
        parsed_data = request.json
        m_id = parsed_data.get('id', None)
        MenuService.deleted(m_id)
    except Exception as err:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()


@bp.route('/setMenuViews', methods=['POST'])
@json_required
def set_menu_views():
    """
    设置菜单访问量
    :return:
    """
    try:
        MenuService.set_menu_views(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
    return partner_success()
