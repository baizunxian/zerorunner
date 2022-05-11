from marshmallow import Schema, fields, EXCLUDE, post_load, pre_load

from autotest.models.sys_models import Lookup, LookupValue
from autotest.serialize.base_serialize import BaseListSchema


class LookupQuerySchema(Schema):
    """字典查询"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    code = fields.Str()
    description = fields.Str()


class LookupListSchema(BaseListSchema):
    """字典列表"""
    id = fields.Int()
    code = fields.Str()
    description = fields.Str()


class LookupSaveOrUpdateSchema(BaseListSchema):
    """字典保存"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    code = fields.Str()
    description = fields.Str()

    @post_load
    def post_load(self, data, **kwargs):
        id = data.get("id", None)
        code = data.get("code", None)
        if not data.get("code"):
            raise ValueError("字典code不能为空!")
        if id:
            lookup = Lookup.get(id)
            if not lookup:
                raise ValueError("字典不存在!")
            if lookup.code != code:
                if Lookup.get_list(code=code).first():
                    raise ValueError("字典code已存在!")
        else:
            if Lookup.get_list(code=code).first():
                raise ValueError("字典code已存在!")
        return data


class LookupValueSchema(BaseListSchema):
    """字典值"""
    id = fields.Int()
    lookup_id = fields.Int()
    lookup_code = fields.Str()
    lookup_value = fields.Str()
    ext = fields.Str()
    display_sequence = fields.Str()
    description = fields.Str()
    code = fields.Str()


class LookupValueDictSchema(BaseListSchema):
    """所有字段值"""
    id = fields.Int()
    lookup_id = fields.Int()
    lookup_code = fields.Str()
    lookup_value = fields.Str()
    code = fields.Str()


class LookupValueQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    code = fields.Str()
    lookup_id = fields.Int()

    @post_load
    def post_load(self, data, **kwargs):
        code = data.get('code', None)
        lookup_id = data.get('lookup_id', None)
        if not code:
            raise ValueError('编码不能为空！')
        if not lookup_id:
            raise ValueError('数据字典id不能为空！')
        return data


class LookupValueSaveOrUpdateSchema(BaseListSchema):
    """字典值保存"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    lookup_id = fields.Int()
    lookup_code = fields.Str()
    lookup_value = fields.Str()
    ext = fields.Str(allow_none=True)
    display_sequence = fields.Int()
    description = fields.Str(allow_none=True)

    @pre_load
    def pre_load(self, data, **kwargs):
        display_sequence = data.get("display_sequence", None)
        if not display_sequence:
            raise ValueError("显示顺序不能为空！")
        return data

    @post_load
    def post_load(self, data, **kwargs):
        id = data.get("id", None)
        lookup_id = data.get("lookup_id", None)
        lookup_code = data.get("lookup_code", None)
        if not lookup_id:
            raise ValueError("字典id不能为空！")
        if id:
            lookup_value = LookupValue.get(id)
            if not lookup_value:
                raise ValueError("字典id不存在!")
            if lookup_value.lookup_code != lookup_code:
                if LookupValue.get_lookup_value_by_lookup_id(lookup_id=lookup_id, lookup_code=lookup_code).first():
                    raise ValueError("数据字典值的value以及编码已经存在!")
        else:
            if LookupValue.get_lookup_value_by_lookup_id(lookup_id=lookup_id, lookup_code=lookup_code).first():
                raise ValueError("数据字典值的value以及编码已经存在!")
        return data
