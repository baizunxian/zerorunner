from typing import Optional, Text, List

from pydantic import root_validator

from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class RoleQuerySchema(BaseQuerySchema):
    """角色查询序列化"""

    id: Optional[int]
    name: Optional[Text]


class RoleListSchema(BaseListSchema):
    """角色序列化"""
    name: Optional[Text]
    role_type: Optional[int]
    menus: Optional[List[int]]
    description: Optional[Text]
    status: Optional[int]

    @root_validator(pre=True)
    def pre_load(cls, data):
        menus = data.get("menus", None)
        if menus and isinstance(menus, str):
            data["menus"] = list(map(int, data["menus"].split(',')))
        return data
