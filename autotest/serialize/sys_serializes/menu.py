from marshmallow import fields

from autotest.serialize.base_serialize import BaseListSchema


class MenuListSchema(BaseListSchema):
    """菜单序列化"""
    id = fields.Int()
    path = fields.Str()
    component = fields.Str()
    title = fields.Str()
    name = fields.Str()
    isLink = fields.Boolean()
    isHide = fields.Boolean()
    isKeepAlive = fields.Boolean()
    isAffix = fields.Boolean()
    isIframe = fields.Boolean()
    roles = fields.Str()
    icon = fields.Str()
    parent_id = fields.Int()
    redirect = fields.Str()
    sort = fields.Int()
    menu_type = fields.Int()
    lookup_id = fields.Int()
    active_menu = fields.Str()
