# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53

"""
Built-in validate comparators.
"""

import re
import typing


def equal(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert check_value == expect_value, message


def greater_than(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    assert check_value > expect_value, message


def less_than(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    assert check_value < expect_value, message


def greater_or_equals(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    assert check_value >= expect_value, message


def less_or_equals(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    assert check_value <= expect_value, message


def not_equal(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert check_value != expect_value, message


def string_equals(check_value: str, expect_value: typing.Any, message: str = ""):
    assert str(check_value) == str(expect_value), message


def length_equal(check_value: str, expect_value: int, message: str = ""):
    assert isinstance(expect_value, int), "expect_value should be int type"
    assert len(check_value) == expect_value, message


def length_greater_than(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) > expect_value, message


def length_greater_or_equals(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) >= expect_value, message


def length_less_than(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) < expect_value, message


def length_less_or_equals(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) <= expect_value, message


def contains(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert isinstance(
        check_value, (list, tuple, dict, str, bytes)
    ), "expect_value should be list/tuple/dict/str/bytes type"
    assert expect_value in check_value, message


def contained_by(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)
    ), "expect_value should be list/tuple/dict/str/bytes type"
    assert check_value in expect_value, message


def type_match(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, str):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    if expect_value in ["None", "NoneType", None]:
        assert check_value is None, message
    else:
        assert type(check_value) == get_type(expect_value), message


def regex_match(check_value: str, expect_value: typing.Any, message: str = ""):
    assert isinstance(expect_value, str), "expect_value should be Text type"
    assert isinstance(check_value, str), "check_value should be Text type"
    assert re.match(expect_value, check_value), message


def startswith(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert str(check_value).startswith(str(expect_value)), message


def endswith(check_value: str, expect_value: typing.Any, message: str = ""):
    assert str(check_value).endswith(str(expect_value)), message
