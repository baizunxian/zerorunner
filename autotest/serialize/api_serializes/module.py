from marshmallow import Schema, EXCLUDE, fields

from autotest.serialize.base_serialize import BaseListSchema


class ModuleQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    name = fields.Str()
    project_name = fields.Str()
    project_id = fields.Int()
    order_field = fields.Str()
    sort_type = fields.Int()
    created_by_name = fields.Str()


class ModuleListSchema(BaseListSchema):
    """模块序列化"""
    id = fields.Int()
    name = fields.Str()
    project_id = fields.Int()
    project_name = fields.Str()
    config_id = fields.Int()
    test_user = fields.Str()
    simple_desc = fields.Str()
    remarks = fields.Str()
    leader_user = fields.Str()
    priority = fields.Int()
    module_packages = fields.Str()
    packages_id = fields.Int()
    case_count = fields.Int()
