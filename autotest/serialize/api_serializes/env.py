from marshmallow import Schema, EXCLUDE, fields, post_load

from autotest.models.api_models import Env
from autotest.serialize.base_serialize import BaseListSchema


class EnvQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    name = fields.Str()
    created_by_name = fields.Str()


class EnvListSchema(BaseListSchema):
    """环境序列化"""
    id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    remarks = fields.Str()


class EnvSaveOrUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    name = fields.Str()
    url = fields.Str()
    remarks = fields.Str(allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        e_id = data.get('id', None)
        e_name = data.get('name', None)
        e_url = data.get('url', None)

        if not e_name:
            raise ValueError('环境名称不能为空')
        else:
            if Env.get_list(name=e_name).first():
                raise ValueError("环境名称已存在!")
        if not e_url:
            raise ValueError('环境地址不能为空')

        # 判断名称是否重复
        if e_id:
            env = Env.get(e_id)
            if not env:
                raise ValueError("数据跟新失败，环境不存在！")
            if env.name != e_name:
                if env.get_list(name=e_name).first():
                    raise ValueError("环境名称已存在!")
        return data
