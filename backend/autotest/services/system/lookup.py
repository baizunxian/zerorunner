import typing
from autotest.utils.response.codes import CodeEnum
from autotest.exceptions.exceptions import ParameterError
from autotest.models.system_models import Lookup, LookupValue
from autotest.schemas.system.lookup import LookupIn, LookupValueIn, LookupQuery, LookupId, LookupValueQuery


class LookupService:
    """数据字典"""

    @staticmethod
    async def list(params: LookupQuery) -> typing.Dict[typing.Text, typing.Any]:
        data = await Lookup.get_list(params)
        return data

    @staticmethod
    async def save_or_update(params: LookupIn) -> typing.Dict[typing.Text, typing.Any]:
        if not params.code:
            raise ParameterError(CodeEnum.LOOKUP_CODE_NOT_EMPTY)
        if params.id:
            lookup = await Lookup.get(params.id)
            if not lookup:
                raise ParameterError(CodeEnum.LOOKUP_NOT_EXIST)
            if lookup.code != params.code:
                if await Lookup.get_lookup_by_code(code=params.code):
                    raise ParameterError(CodeEnum.LOOKUP_CODE_EXIST)
        else:
            if await Lookup.get_lookup_by_code(code=params.code):
                raise ParameterError(CodeEnum.LOOKUP_CODE_EXIST)

        return await Lookup.create_or_update(params.dict())

    @staticmethod
    async def deleted(params: LookupId):
        if await LookupValue.get_lookup_value(LookupValueQuery(lookup_id=params.id)):
            raise ParameterError('数据字典类型不能直接删除，请先解除数据字典类型与数据字典关联')
        return await Lookup.delete(params.id)


class LookupValueService:

    @staticmethod
    async def get_all_lookup() -> typing.Dict[typing.Text, typing.Any]:
        """获取所有数据字典"""
        all_lookup_value = await LookupValue.get_lookup_value()
        lookup_dict = {}
        if not all_lookup_value:
            return lookup_dict
        for lookup_info in all_lookup_value:
            code = lookup_info["code"]
            lookup_code = lookup_info["lookup_code"]
            lookup_value = lookup_info["lookup_value"]
            if code not in lookup_dict:
                lookup_dict[code] = {}
            lookup_dict[code].setdefault(lookup_code, lookup_value)
        return lookup_dict

    @staticmethod
    async def get_lookup_value(params: LookupValueQuery) -> typing.List[typing.Any]:
        """获取字典值"""
        lookup_value = await LookupValue.get_lookup_value(params)
        if not lookup_value:
            return []
        return lookup_value

    @staticmethod
    async def save_or_update(params: LookupValueIn) -> typing.Dict[typing.Text, typing.Any]:
        """保存或更新字典值"""

        if not params.display_sequence:
            raise ParameterError("显示顺序不能为空！")

        if not params.lookup_id:
            raise ParameterError("字典id不能为空！")

        exists_lookup_value = await LookupValue.get_lookup_value_by_lookup_id(lookup_id=params.lookup_id,
                                                                              lookup_code=params.lookup_code)

        if params.id:
            lookup_value = await LookupValue.get(params.id)
            if not lookup_value:
                raise ParameterError("字典id不存在!")
            if lookup_value.lookup_code != params.lookup_code and exists_lookup_value:
                raise ParameterError("数据字典值的value以及编码已经存在!")
        else:
            if await LookupValue.get_lookup_value_by_lookup_id(lookup_id=params.lookup_id,
                                                               lookup_code=params.lookup_code):
                raise ParameterError("数据字典值的value以及编码已经存在!")
        return await LookupValue.create_or_update(params.dict())

    @staticmethod
    async def deleted(params: LookupId):
        """删除字典值"""
        return await LookupValue.delete(params.id)
