from marshmallow import Schema, fields


class BaseListSchema(Schema):
    """列表返回数据固定字段"""

    enabled_flag = fields.Int()
    created_by = fields.Int(allow_none=True)
    updated_by = fields.Int(allow_none=True)
    created_by_name = fields.Str(allow_none=True)
    updated_by_name = fields.Str(allow_none=True)
    creation_date = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))
    updation_date = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))
