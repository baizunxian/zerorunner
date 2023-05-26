import inspect
import os
import typing
import uuid
from types import FunctionType

from autotest.models.api_models import Functions
from autotest.schemas.api.functions import FuncQuery, FuncIn, FuncDebug, FuncListQuery, FuncId
from config import config
from zerorunner.loader import load_func_content
from zerorunner.parser import get_mapping_function, parse_string_value


class FunctionsService:
    """自定义函数类"""

    @staticmethod
    async def list(params: FuncQuery) -> typing.Dict:
        """
        获取函数列表
        :param params: 参数
        :return:
        """
        data = await Functions.get_list(params)

        return data

    @staticmethod
    async def get_function_info(params: FuncQuery) -> typing.Dict:
        """
        获取自定义函数信息
        :param params:
        :return:
        """
        common = params.common
        if common and common == 'common':
            path = config.BASEDIR
            function_path = os.path.join(path, 'utils', 'basic_function.py')
            w = open(function_path, encoding='utf8')
            basic_function = w.read()
            data = {
                'content': basic_function,
                'name': '公共函数',
                'edit': False,
            }
            return data
        function_info = await Functions.get_by_id(params.id)
        if not function_info:
            raise ValueError("脚本不存在！")
        function_info['edit'] = True
        return function_info

    @staticmethod
    async def save_or_update(params: FuncIn) -> typing.Dict:
        """
        自定义函数保存方法
        :param params:
        :return:
        """
        load_func_content(content=params.content, module_name=uuid.uuid4().hex)
        data = await Functions.create_or_update(params.dict())
        return data

    @staticmethod
    async def debug_func(params: FuncDebug) -> typing.Any:
        """
        调试函数
        :param params: 参数
        :return:
        """
        try:
            data = await FunctionsService.get_function_by_id(FuncListQuery(id=params.id))
            functions_mapping = data.get('functions_mapping')
            func = get_mapping_function(params.func_name, functions_mapping)
            if not func:
                raise ValueError('未匹配到函数！')
            args_info = {key: parse_string_value(value) for key, value in params.args_info.items()}
            result = func(**args_info)
            return result
        except Exception as err:
            raise ValueError(f"函数调试错误：{str(err)}")

    @staticmethod
    async def get_function_by_id(params: FuncListQuery) -> typing.Dict:
        """
        获取函数信息
        :param params: 参数
        :return:
        """
        file_info = await FunctionsService.handle_func_content(params.id)
        content = file_info.get('content', '')
        common_content = file_info.get('common_content', '')
        # modules = importlib.import_module('autotest.utils.basic_function', __name__)
        functions_mapping = load_func_content(f"{common_content}\n{content}", f"{params.id}_{uuid.uuid4().__hash__()}")
        func_list = []
        for func_name, func in functions_mapping.items():
            if not params.id:
                file_content = common_content
            else:
                file_content = content
            if file_content.find(f'def {func_name}(') == -1:
                continue
            if params.func_name:
                if params.func_name in func.__name__ or params.func_name in func.__doc__ if func.__doc__ else '':
                    func_list.append(FunctionsService.handle_func_info(func))
            else:
                func_list.append(FunctionsService.handle_func_info(func))
        func_data = {
            'func_list': func_list,
            'functions_mapping': functions_mapping,
        }
        return func_data

    @staticmethod
    async def handle_func_content(func_id: typing.Union[int, str, None]) -> typing.Dict:
        """
        处理函数
        :param func_id:
        :return:
        """
        common_func_path = os.path.join(config.BASEDIR, 'autotest', 'utils', 'basic_function.py')
        common_content = ''
        if os.path.exists(common_func_path):
            w = open(common_func_path, encoding='utf8')
            common_content = w.read()
        content = ''
        if func_id:
            func_info = await Functions.get(func_id)
            if func_info:
                content = func_info.content if func_info.content else ''
        data = {
            'content': content,
            'common_content': common_content
        }
        return data

    @staticmethod
    def handle_func_info(func: FunctionType) -> typing.Dict:
        """
        处理函数返回函数信息
        :param func:
        :return:
        """
        func_info = inspect.signature(func)
        parameters = func_info.parameters
        args_dict = dict()
        for name, param_info in parameters.items():
            args_dict.setdefault(name, param_info.default if not isinstance(param_info.default, type) else '')

        return dict(
            func_name=func.__name__,
            func_args=str(func_info),
            args_info=args_dict,
            func_doc=func.__doc__,
        )

    @staticmethod
    async def deleted(params: FuncId):
        """删除"""
        return await Functions.delete(params.id)
