import traceback
from typing import Dict, Any, Text

from loguru import logger

from autotest.models.sys_models import User, Roles
from autotest.serialize.sys_serializes.role import (RoleListSchema, RoleQuerySchema)
from autotest.utils.api import parse_pagination


class RolesService:
    """角色类"""

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        query_data = RoleQuerySchema().load(kwargs)
        data = parse_pagination(Roles.get_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        _result = RoleListSchema().dump(_result, many=True)
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "Roles":
        id = kwargs.get('id', None)
        name = kwargs.get('name', None)
        menus = kwargs.get('menus', None)
        role_info = Roles.get(id) if id else Roles()
        if role_info.id:
            if role_info.name != name:
                if Roles.get_roles_by_name(name):
                    raise ValueError('角色名已存在!')
        if kwargs.get('menus', ''):
            kwargs['menus'] = ','.join(list(map(str, menus)))
        role_info.update(**kwargs)
        return role_info

    @staticmethod
    def deleted(id: int):
        try:
            users = User.get_user_by_roles(id)
            if users:
                raise ValueError('有用户关联了当前角色，不允许删除!')
            role = Roles.get(id)
            role.delete() if role else ...
        except Exception as err:
            logger.error(traceback.format_exc())
