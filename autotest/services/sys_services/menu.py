import traceback
from typing import Dict, Any, List, Text

from flask import request
from loguru import logger

from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.models.sys_models import Menu
from autotest.serialize.sys_serializes.menu import MenuListSchema


class MenuService:
    """菜单类"""

    @staticmethod
    def all_menu() -> List[Any]:
        """平铺菜单"""
        return MenuListSchema().dump(Menu.get_all(), many=True)

    @staticmethod
    def all_menu_nesting() -> List[Any]:
        """嵌套菜单"""
        all_menu = MenuListSchema().dump(Menu.get_all(), many=True)
        parent_menu = [menu for menu in all_menu if menu['parent_id'] == 0]
        result = MenuService.menu_assembly(parent_menu, all_menu)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "Menu":
        menu_id = kwargs.get('id', None)
        title = kwargs.get('title', None)
        menu_info = Menu.get(menu_id) if menu_id else Menu()
        if menu_info.id:
            if menu_info.title != title:
                if Menu.get_menu_by_name(title):
                    raise ValueError('菜单名已存在！')
        menu_info.update(**kwargs)
        return menu_info

    @staticmethod
    def deleted(id: int):
        menu = Menu.get(id)
        menus = Menu.get_menu_by_parent(id)
        if menus:
            raise ValueError(partner_errmsg.get(codes.MENU_HAS_MODULE_ASSOCIATION))
        menu.delete() if menu else ...

    @staticmethod
    def set_menu_views(**kwargs: Any):
        m_id = kwargs.get('menu_id', None)
        user_id = kwargs.get('user_id', None)
        remote_addr = request.headers.get("X-Real-Ip", None)
        remote_ip = request.remote_addr
        if not m_id:
            return
        menu = Menu.get(m_id)
        if menu:
            try:
                logger.info(f"[{user_id}] IP {remote_addr} 访问了[{menu.title}]菜单")
                menu.views = menu.views + 1 if menu.views else 1
                menu.save()
                # 菜单浏览
                # menu_view = MenuViewHistory()
                # menu_view.menu_id = m_id
                # menu_view.remote_addr = remote_addr if remote_addr else remote_ip
                # menu_view.user_id = user_id
                # menu_view.save()
            except Exception as err:
                logger.error(traceback.format_exc())

    @staticmethod
    def assemble_menu_data(menu: Dict[Text, Any]) -> Dict[Text, Any]:
        """
        菜单组装
        :param menu:
        :return:
        """
        if not menu.get('meta', None):
            menu['meta'] = {
                'title': menu.get('title', None),
                'isLink': menu.pop('isLink', None),
                'isHide': menu.pop('isHide', None),
                'isKeepAlive': menu.pop('isKeepAlive', None),
                'isAffix': menu.pop('isAffix', None),
                'isIframe': menu.pop('isIframe', None),
                'icon': menu.pop('icon', None),
                'roles': ['all']
            }
        return menu

    @staticmethod
    def menu_assembly(parent_menu: List[Any], all_menu: List[Any]) -> List[Any]:
        """
        递归遍历菜单
        :param parent_menu: 一级菜单列表
        :param all_menu: 所有菜单
        :return:
        """
        for parent in parent_menu:
            MenuService.assemble_menu_data(parent)
            for menu in all_menu:
                if menu['parent_id'] == parent['id']:
                    parent['children'] = [] if not parent.get('children', None) else parent['children']
                    MenuService.assemble_menu_data(menu)
                    parent['children'].append(menu)
            MenuService.menu_assembly(parent['children'], all_menu) if parent.get('children', None) else ...
        return parent_menu
