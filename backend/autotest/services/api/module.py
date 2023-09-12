import typing

from autotest.utils.response.codes import CodeEnum
from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ModuleInfo, ApiInfo
from autotest.schemas.api.module import ModuleQuery, ModuleIn, ModuleId


class ModuleService:
    """模块处理类"""

    @staticmethod
    async def list(params: ModuleQuery) -> typing.Dict:
        """
        获取模块列表
        :param params: 查询参数
        :return:
        """
        data = await ModuleInfo.get_list(params)
        return data

    @staticmethod
    async def get_all() -> typing.Dict:
        """
        获取模块列表
        :return:
        """
        data = await ModuleInfo.get_all()
        return data

    @staticmethod
    async def save_or_update(params: ModuleIn) -> typing.Dict:
        """
        模块保存方法
        :param params: 参数
        :return:
        """
        # 当模块关联的包发生变更时，原始包移除模块信息
        same_name_module = await ModuleInfo.get_module_by_name(params.name)
        if params.id:
            module_info = await ModuleInfo.get(params.id)
            if module_info.name != params.name:
                if await ModuleInfo.get_module_by_name(params.name):
                    raise ParameterError(CodeEnum.MODULE_NAME_EXIST)
        else:
            if same_name_module:
                raise ParameterError(CodeEnum.MODULE_NAME_EXIST)
        return await ModuleInfo.create_or_update(params.dict())

    @staticmethod
    async def deleted(params: ModuleId):
        """
        删除模块
        :param params:
        :return:
        """
        if params.id:
            relation_api = await ApiInfo.get_api_by_module_id(params.id)
            if relation_api:
                raise ParameterError(CodeEnum.MODULE_HAS_CASE_ASSOCIATION)
            return await ModuleInfo.delete(params.id)
