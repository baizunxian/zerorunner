# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import contextlib
import csv
import importlib
import os
import sys
import traceback
import types
import typing
from io import StringIO

from loguru import logger

from zerorunner import exceptions
from zerorunner import builtin


def load_csv_file(csv_file: str) -> typing.List[typing.Dict]:
    """ 加载csv文件

    Args:
        csv_file (str): csv file path, csv file content is like below:

    Returns:
        list: list of parameters, each parameter is in dict format

    Examples:
        >>> cat csv_file
        username,password
        test1,111111
        test2,222222
        test3,333333

        >>> load_csv_file(csv_file)
        [
            {'username': 'test1', 'password': '111111'},
            {'username': 'test2', 'password': '222222'},
            {'username': 'test3', 'password': '333333'}
        ]

    """

    if not os.path.isfile(csv_file):
        # file path not exist
        raise exceptions.CSVNotFound(csv_file)

    csv_content_list = []

    with open(csv_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_content_list.append(row)

    return csv_content_list


def load_module_functions(module) -> typing.Dict[str, typing.Callable]:
    """ 加载python模块函数
    Args:
        module: python 模块
    Returns:
        dict: python函数字典

            {
                "func1_name": func1,
                "func2_name": func2
            }

    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def load_builtin_functions() -> typing.Dict[str, typing.Callable]:
    """ 加载内置函数
    """
    return load_module_functions(builtin)


def load_func_content(content: str, module_name: str) -> typing.Dict[str, typing.Callable]:
    """
    args:
        content: python 脚本Text
        module_name: module 名称
    """
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    try:
        code = compile(content, module_name, 'exec')
        exec(code, mod.__dict__)
        imported_module = importlib.import_module(module_name)
    except IndentationError:
        raise IndentationError(f"格式错误，请检查！\n {traceback.format_exc()}")
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"模块导入错误！\n {traceback.format_exc()}")
    except Exception:
        raise Exception(f"脚本错误！\n {traceback.format_exc()}")
    return load_module_functions(imported_module)


def load_script_content(content: str, module_name: str, params: dict = None) -> [types.ModuleType, StringIO]:
    """执行脚本"""
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    output_buffer = StringIO()
    log_handler = CapturingLogHandler(output_buffer)
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{line}</cyan> | <level>{message}</level>"
    temp_logger = logger.add(log_handler, format=fmt)

    if not params:
        params = {}
    if "requests" not in params:
        import requests
        params["requests"] = requests
    params["logger"] = logger
    if params:
        mod.__dict__.update(params)
    try:
        code = compile(content, module_name, 'exec')
        with contextlib.redirect_stdout(output_buffer):
            exec(code, mod.__dict__)
        captured_output = output_buffer.getvalue()
        return mod, captured_output
    except IndentationError:
        raise IndentationError(f"脚本格式错误，请检查！\n {traceback.format_exc()}")

    finally:
        logger.remove(temp_logger)
        output_buffer.close()


class CapturingLogHandler:
    def __init__(self, output_buffer):
        self.output_buffer = output_buffer

    def write(self, message):
        self.output_buffer.write(message)
