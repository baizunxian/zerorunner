from typing import Optional, Text
from pydantic import root_validator

from autotest.exc.exceptions import ParameterError
from autotest.models.sys_models import Lookup, LookupValue
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class LookupSaveOrUpdateSchema(BaseListSchema):
    """字典保存"""

    code: Optional[Text]
    description: Optional[Text]

    @root_validator(pre=True)
    def root_validator(cls, data):
        id = data.get("id", None)
        code = data.get("code", None)
        if not data.get("code"):
            raise ParameterError("字典code不能为空!")
        if id:
            lookup = Lookup.get(id)
            if not lookup:
                raise ParameterError("字典不存在!")
            if lookup.code != code:
                if Lookup.get_list(code=code).first():
                    raise ParameterError("字典code已存在!")
        else:
            if Lookup.get_list(code=code).first():
                raise ParameterError("字典code已存在!")
        return data


class LookupValueQuerySchema(BaseQuerySchema):
    code: Optional[Text]
    lookup_id: Optional[int]

    @root_validator(pre=True)
    def root_validator(cls, data):
        code = data.get('code', None)
        lookup_id = data.get('lookup_id', None)
        if not code:
            raise ParameterError('编码不能为空！')
        if not lookup_id:
            raise ParameterError('数据字典id不能为空！')
        return data


class LookupValueSaveOrUpdateSchema(BaseListSchema):
    """字典值保存"""

    lookup_id: Optional[int]
    lookup_code: Optional[Text]
    lookup_value: Optional[Text]
    ext: Optional[Text]
    display_sequence: Optional[int]
    description: Optional[Text]

    @root_validator(pre=True)
    def pre_load(cls, data):
        display_sequence = data.get("display_sequence", None)
        if not display_sequence:
            raise ParameterError("显示顺序不能为空！")
        return data

    @root_validator
    def post_load(cls, data):
        id = data.get("id", None)
        lookup_id = data.get("lookup_id", None)
        lookup_code = data.get("lookup_code", None)
        if not lookup_id:
            raise ParameterError("字典id不能为空！")
        if id:
            lookup_value = LookupValue.get(id)
            if not lookup_value:
                raise ParameterError("字典id不存在!")
            if lookup_value.lookup_code != lookup_code:
                if LookupValue.get_lookup_value_by_lookup_id(lookup_id=lookup_id, lookup_code=lookup_code).first():
                    raise ParameterError("数据字典值的value以及编码已经存在!")
        else:
            if LookupValue.get_lookup_value_by_lookup_id(lookup_id=lookup_id, lookup_code=lookup_code).first():
                raise ParameterError("数据字典值的value以及编码已经存在!")
        return data
