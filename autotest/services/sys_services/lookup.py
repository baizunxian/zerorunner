from typing import Dict, Any, Text, List

from autotest.models.sys_models import Lookup, LookupValue
from autotest.serialize.sys_serializes.lookup import LookupListSchema, LookupSaveOrUpdateSchema, LookupValueSchema, \
    LookupValueQuerySchema, LookupValueSaveOrUpdateSchema, LookupValueDictSchema
from autotest.utils.api import parse_pagination


class LookupService:
    """数据字典"""

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        code = kwargs.get('code', None)
        data = parse_pagination(Lookup.get_list(code))
        _result, pagination = data.get('result'), data.get('pagination')
        _result = LookupListSchema().dump(_result, many=True)
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "Lookup":
        parsed_data = LookupSaveOrUpdateSchema().load(kwargs)
        id = parsed_data.get('id', None)
        lookup = Lookup.get(id) if id else Lookup()
        lookup.update(**parsed_data)
        return lookup

    @staticmethod
    def deleted(lookup_id: int):
        if LookupValue.get_lookup_value(lookup_id=lookup_id).first():
            raise ValueError('数据字典类型不能直接删除，请先解除数据字典类型与数据字典关联')
        lookup = Lookup.get(lookup_id).delete()
        lookup.delete() if lookup else ...


class LookupValueService:

    @staticmethod
    def get_all_lookup() -> Dict[Text, Any]:
        """获取所有数据字典"""
        all_lookup_value = LookupValue.get_lookup_value().all()
        lookup_dict = {}
        for lookup_info in all_lookup_value:
            if lookup_info.code not in lookup_dict:
                lookup_dict[lookup_info.code] = {}
                lookup_dict[lookup_info.code].setdefault(lookup_info.lookup_code, lookup_info.lookup_value)
            else:
                lookup_dict[lookup_info.code].setdefault(lookup_info.lookup_code, lookup_info.lookup_value)
        return lookup_dict

    @staticmethod
    def get_lookup_value(**kwargs: Any) -> List[Any]:
        """获取字典值"""
        parsed_data = LookupValueQuerySchema().load(kwargs)
        code = parsed_data.get('code', None)
        lookup_id = parsed_data.get('lookup_id', None)
        lookup_value = LookupValue.get_lookup_value(code, lookup_id).all()
        if not lookup_value:
            return []
        lookup_value = LookupValueSchema().dump(lookup_value, many=True)
        return lookup_value

    @staticmethod
    def save_or_update(**kwargs: Any) -> "LookupValue":
        """保存或更新字典值"""
        parsed_data = LookupValueSaveOrUpdateSchema().load(kwargs)
        id = parsed_data.get('id', None)
        lookup_value_info = LookupValue.get(id) if id else LookupValue()
        lookup_value_info.update(**parsed_data)
        return lookup_value_info

    @staticmethod
    def deleted(lookup_value_id: int):
        """删除字典值"""
        lookup_value_info = LookupValue.get(lookup_value_id)
        lookup_value_info.delete() if lookup_value_info else ...
