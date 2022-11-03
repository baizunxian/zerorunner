from flask import Blueprint, request

from autotest.services.sys_services.menu import MenuService
from autotest.utils.api import partner_success

bp = Blueprint('menu', __name__, url_prefix='/api/menu')


@bp.route('/allMenu', methods=['POST'])
def all_menu():
    """
    获取所有菜单数据
    :return:
    """
    data = MenuService.all_menu()
    return partner_success(data=data)


@bp.route('/getAllMenus', methods=['POST'])
def get_all_menus():
    """
    获取结构菜单，父子关系
    :return:
    """
    data = MenuService.all_menu_nesting()
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    新增或者更新menu
    :return:
    """
    # return partner_success(code=codes.PARTNER_CODE_FAIL, msg="演示环境不保存！")
    MenuService.save_or_update(**request.json)
    return partner_success()


@bp.route('/deleted', methods=['POST'])
def delete_menu():
    """
    删除菜单
    :return:
    """
    parsed_data = request.json
    m_id = parsed_data.get('id', None)
    MenuService.deleted(m_id)
    return partner_success()


@bp.route('/setMenuViews', methods=['POST'])
def set_menu_views():
    """
    设置菜单访问量
    :return:
    """
    MenuService.set_menu_views(**request.json)
    return partner_success()
