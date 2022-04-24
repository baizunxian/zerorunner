from marshmallow import Schema, fields, EXCLUDE

from autotest.serialize.base_serialize import BaseListSchema


class DebugTalkQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    project_name = fields.Str()
    name = fields.Str()
    common = fields.Str()


class DebugTalkListSchema(BaseListSchema):
    """自定义函数"""
    id = fields.Int()
    project_id = fields.Int()
    project_name = fields.Str()
    debug_talk = fields.Str()


class DebugTalkSaveOrUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    debug_talk = fields.Str()
    project_id = fields.Str()


class DebugTalkDebugSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    func_parse_str = fields.Str()
    func_name = fields.Str()
    args_info = fields.Dict()
