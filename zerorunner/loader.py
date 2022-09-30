# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

import csv
import importlib
import os
import sys
import traceback
import types
from typing import Callable, Dict, List, Text
import exceptions
import builtin


def load_csv_file(csv_file: Text) -> List[Dict]:
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


def load_module_functions(module) -> Dict[Text, Callable]:
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


def load_builtin_functions() -> Dict[Text, Callable]:
    """ 加载内置函数
    """
    return load_module_functions(builtin)


def load_func_content(content: Text, module_name: Text,  func_type: Text) -> Dict[Text, Callable]:
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
        raise IndentationError(f"脚本格式错误，请检查！\n {traceback.format_exc()}")
    return load_module_functions(imported_module)


def load_script_content(content: Text, module_name: Text) -> types.ModuleType:
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    try:
        code = compile(content, module_name, 'exec')
        exec(code, mod.__dict__)
        return mod
    except IndentationError:
        raise IndentationError(f"脚本格式错误，请检查！\n {traceback.format_exc()}")
