import typing

from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import Env, EnvDataSource, EnvFunc
from autotest.schemas.api.env import EnvQuery, EnvIn, EnvId, BindingDataSourceIn, EnvIdIn, BindingFuncIn


class EnvService:
    @staticmethod
    async def list(params: EnvQuery) -> typing.Dict:
        """
        获取环境列表
        :param params:
        :return:
        """
        data = await Env.get_list(params)
        return data

    @staticmethod
    async def get_all() -> typing.Dict:
        """
        获取环境列表
        :return:
        """
        data = await Env.get_all()
        return data

    @staticmethod
    async def get_env_by_id(params: EnvQuery) -> Env:
        """
        获取环境列表
        :param params:
        :return:
        """
        if not params.id:
            raise ParameterError("id 不能为空!")
        env_info = await Env.get(params.id)
        if not env_info:
            raise ValueError("当前不存在！")
        return env_info

    @staticmethod
    async def save_or_update(params: EnvIn) -> typing.Dict:
        """
        保存更新环境
        :param params:
        :return:
        """
        if not params.name:
            raise ParameterError('环境名称不能为空')

        if not params.domain_name:
            raise ParameterError('环境地址不能为空')
        exist_env = await Env.get_env_by_name(name=params.name)

        # 判断名称是否重复
        if params.id:
            env = await Env.get(params.id)
            if not env:
                raise ParameterError("数据跟新失败，环境不存在！")
            if env.name != params.name and exist_env:
                raise ParameterError("环境名称已存在!")
        else:
            if exist_env:
                raise ParameterError("环境名称已存在!")

        result = await Env.create_or_update(params.dict())
        return result

    @staticmethod
    async def deleted(params: EnvId) -> int:
        """
        删除环境
        :param params:
        :return:
        """
        return await Env.delete(params.id)


class EnvDataSourceService:
    """环境与数据源绑定"""

    @staticmethod
    async def get_by_env_id(params: EnvIdIn):
        """获取环境绑定的数据源"""
        data = await EnvDataSource.get_by_env_id(params.env_id)
        return data if data else []

    @staticmethod
    async def binding_data_source(params: BindingDataSourceIn):
        """环境绑定数据源"""
        bind_list = await EnvDataSourceService.get_by_env_id(EnvIdIn(env_id=params.env_id))
        data_source_ids = [b.get("data_source_id") for b in bind_list if 'data_source_id' in b]
        insert_data = [{"env_id": params.env_id, "data_source_id": source_id} for source_id in params.data_source_ids if
                       source_id not in data_source_ids]
        return await EnvDataSource.batch_create(insert_data)

    @staticmethod
    async def unbinding_data_source(params: BindingDataSourceIn):
        """环境解绑数据源"""
        return await EnvDataSource.unbinding_data_source(params)


class EnvFuncService:
    """环境与辅助函数"""

    @staticmethod
    async def get_by_env_id(params: EnvIdIn):
        """获取环境绑定的辅助函数"""
        data = await EnvFunc.get_by_env_id(params.env_id)
        return data if data else []

    @staticmethod
    async def binding_funcs(params: BindingFuncIn):
        """环境绑定辅助函数"""
        bind_list = await EnvFuncService.get_by_env_id(EnvIdIn(env_id=params.env_id))
        func_ids = [b.get("func_id") for b in bind_list if 'func_id' in b]
        insert_data = [{"env_id": params.env_id, "func_id": func_id} for func_id in params.func_ids if
                       func_id not in func_ids]
        return await EnvFunc.batch_create(insert_data)

    @staticmethod
    async def unbinding_funcs(params: BindingFuncIn):
        """环境解绑辅助函数"""
        return await EnvFunc.unbinding_funcs(params)
