from marshmallow import Schema, fields, EXCLUDE, post_dump

from autotest.serialize.base_serialize import BaseListSchema


class UserQuery(Schema):
    """查询序列化"""

    class Meta:
        """
        RAISEValidationError （默认）：如果有任何未知字段，则引发 err
        EXCLUDE: 排除未知字段
        INCLUDE：接受并包含未知字段
        """
        unknown = EXCLUDE

    id = fields.Int()
    user_ids = fields.List(fields.Str() or fields.Int())
    username = fields.Str()
    nickname = fields.Str()


class UserListSchema(BaseListSchema):
    """用户"""

    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    roles = fields.Str()
    status = fields.Int()
    nickname = fields.Str()
    user_type = fields.Int()
    remarks = fields.Str()

    @post_dump
    def post_dump(self, data, **kwargs):
        """"""
        if 'roles' in data:
            data['roles'] = list(map(int, (data['roles'].split(',')))) if data['roles'] else []
        return data


class UserRegisterSchema(Schema):
    class Meta:
        """
        RAISEValidationError （默认）：如果有任何未知字段，则引发 err
        EXCLUDE: 排除未知字段
        INCLUDE：接受并包含未知字段
        """
        unknown = EXCLUDE

    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str()
    link = fields.Str()
