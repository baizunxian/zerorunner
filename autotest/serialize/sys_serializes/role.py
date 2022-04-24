from marshmallow import Schema, fields, EXCLUDE

from autotest.serialize.base_serialize import BaseListSchema


class RoleQuerySchema(Schema):
    """角色查询序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    name = fields.Str()


class RoleListSchema(BaseListSchema):
    """角色序列化"""
    id = fields.Int()
    name = fields.Str()
    role_type = fields.Int()
    menus = fields.Method('return_menu')
    description = fields.Str()
    status = fields.Int()

    @staticmethod
    def return_menu(obj):
        """
        初始化menus
        source: 1,2,3,4
        target: [1, 2, 3, 4]
        :param obj:
        :return:
        """
        if obj.menus:
            return list(map(int, obj.menus.split(',')))
        return []
