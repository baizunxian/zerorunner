from marshmallow import Schema, fields, EXCLUDE

from autotest.serialize.base_serialize import BaseListSchema


class ProjectQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        """
        RAISEValidationError （默认）：如果有任何未知字段，则引发 err
        EXCLUDE: 排除未知字段
        INCLUDE：接受并包含未知字段
        """
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    name = fields.Str()
    order_field = fields.Str()
    sort_type = fields.Int()
    created_by_name = fields.Str()


class ProjectListSchema(BaseListSchema):
    """项目序列化"""
    id = fields.Int()
    name = fields.Str()
    responsible_name = fields.Str()
    test_user = fields.Str()
    dev_user = fields.Str()
    publish_app = fields.Str()
    simple_desc = fields.Str()
    remarks = fields.Str()
    config_id = fields.Int()
    run_status = fields.Str()
    product_id = fields.Int()
