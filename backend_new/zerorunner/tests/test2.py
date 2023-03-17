# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import inspect
import sys
import traceback
import types
import typing


def load_script_content(content: typing.Text, module_name: typing.Text) -> types.ModuleType:
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    try:
        code = compile(content, module_name, 'exec')
        exec(code, mod.__dict__)
        return mod
    except IndentationError:
        raise IndentationError(f"格式错误，请检查！\n {traceback.format_exc()}")


def test(a='${test}', b=1):
    ...


a = "test(c, ${d}, a='test', b=[1,2,3])"

a = f"def {a}:\n\t\t\t\t'test'"

b = load_script_content(a, 'a')
func_info = inspect.signature(b.test)
parameters = func_info.parameters
print(parameters)
