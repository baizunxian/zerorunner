import traceback
import typing

from loguru import logger

from autotest.models.system_models import Roles, User
from autotest.schemas.system.roles import RoleQuery, RoleIn, RoleDel


class RolesService:
    """角色类"""

    @staticmethod
    async def list(params: RoleQuery) -> typing.Dict[str, typing.Any]:
        data = await Roles.get_list(params)
        for row in data.get("rows", []):
            row["menus"] = list(map(int, (row["menus"].split(",")))) if row["menus"] else []
        return data

    @staticmethod
    async def save_or_update(params: RoleIn) -> int:

        if params.id:
            role_info = await Roles.get(params.id)
            if role_info.name != params.name:
                if await Roles.get_roles_by_name(params.name):
                    raise ValueError('角色名已存在!')
        else:
            if await Roles.get_roles_by_name(params.name):
                raise ValueError('角色名已存在!')
        result = await Roles.create_or_update(params.dict())
        return result

    @staticmethod
    async def deleted(params: RoleDel) -> int:
        try:
            relation_data = await User.get_user_by_roles(params.id)
            if relation_data:
                raise ValueError('有用户关联了当前角色，不允许删除!')
            return await Roles.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
