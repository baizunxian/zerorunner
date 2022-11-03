import inspect
import os
import uuid
from types import FunctionType
from typing import Any, Dict, Union, Text

from autotest.config import config
from autotest.httprunner.parser import get_mapping_function, parse_string_value
from autotest.models.api_models import Functions
from autotest.serialize.api_serializes.functions import FuncSaveOrUpdateSchema, FuncDebugSchema, FuncQuerySchema, \
    FuncListSchema
from autotest.utils.api import parse_pagination
from zerorunner.loader import load_func_content


class FunctionsService:
    """自定义函数类"""

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取函数列表
        :param kwargs:
        :return:
        """
        query_data = FuncQuerySchema(**kwargs).dict()
        data = parse_pagination(Functions.get_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': _result
        }
        result.update(pagination)
        return result

    @staticmethod
    def get_debug_talk_info(**kwargs: Any) -> Dict[Text, Text]:
        """
        获取自定义函数信息
        :param kwargs:
        :return:
        """
        query_data = FuncQuerySchema(**kwargs)
        d_id = query_data.id
        common = query_data.common
        if common and common == 'common':
            path = config.BASEDIR
            function_path = os.path.join(path, 'utils', 'basic_function.py')
            w = open(function_path, encoding='utf8')
            basic_function = w.read()
            data = {
                'content': basic_function,
                'project_name': '公共函数',
                'edit': False,
            }
            return data
        debug_talk_info = Functions.get_by_id(d_id)
        debug_talk_info = FuncListSchema.serialize(debug_talk_info)
        debug_talk_info['edit'] = True
        return debug_talk_info

    @staticmethod
    def save_or_update(**kwargs: Any) -> "Functions":
        """
        自定义函数保存方法
        :param kwargs:
        :return:
        """
        parsed_data = FuncSaveOrUpdateSchema().load(kwargs)
        d_id = parsed_data.get('id', None)
        debug_info = Functions.get(d_id) if d_id else Functions()
        debug_info.update(**kwargs)
        return debug_info

    @staticmethod
    def debug_func(**kwargs: Any) -> Any:
        """
        调试函数
        :param kwargs:
        :return:
        """
        parsed_data = FuncDebugSchema(**kwargs)
        func_id = parsed_data.id
        args_info = parsed_data.args_info
        func_parse_str = parsed_data.func_parse_str
        func_name = parsed_data.func_name
        try:
            data = FunctionsService.get_function_by_path(func_id)
            functions_mapping = data.get('functions_mapping')
            func = get_mapping_function(func_name, functions_mapping)
            if not func:
                raise ValueError('未匹配到函数！')
            args_info = {key: parse_string_value(value) for key, value in args_info.items()}
            result = func(**args_info)
            return result
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def get_function_by_path(func_id: Union[str, int, None] = None, name: Text = None) -> Dict[Text, Any]:
        """
        获取函数信息
        :param func_id:
        :param name:
        :return:
        """
        file_info = FunctionsService.handle_func_content(func_id)
        content = file_info.get('content', '')
        common_content = file_info.get('common_content', '')
        # modules = importlib.import_module('autotest.utils.basic_function', __name__)
        functions_mapping = load_func_content(f"{common_content}\n{content}", f"{func_id}_{uuid.uuid4().__hash__()}")
        func_list = []
        for func_name, func in functions_mapping.items():
            if not func_id:
                file_content = common_content
            else:
                file_content = content
            # if file_content.find(f'def {func_name}(') == -1:
            #     continue
            if name:
                if name in func.__name__ or name in func.__doc__ if func.__doc__ else '':
                    func_list.append(FunctionsService.handle_func_info(func))
            else:
                func_list.append(FunctionsService.handle_func_info(func))
        func_data = {
            'func_list': func_list,
            'functions_mapping': functions_mapping,
        }
        return func_data

    @staticmethod
    def handle_func_content(func_id: Union[int, str, None]) -> Dict[Text, Text]:
        """
        处理函数
        :param func_id:
        :return:
        """
        common_func_path = os.path.join(os.getcwd(), 'autotest', 'utils', 'basic_function.py')
        w = open(common_func_path, encoding='utf8')
        common_content = w.read()
        content = ''
        if func_id:
            func_info = Functions.get(func_id)
            if func_info:
                content = func_info.content if func_info.content else ''
        data = {
            'content': content,
            'common_content': common_content
        }
        return data

    @staticmethod
    def handle_func_info(func: FunctionType) -> Dict[Text, Any]:
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
