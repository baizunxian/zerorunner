# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from datetime import datetime
from json import JSONEncoder

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, select, func, literal_column, Row
from sqlalchemy.orm import noload, DeclarativeMeta

T = typing.TypeVar("T", Select, "Query[Any]")


def count_query(query: Select) -> Select:
    """
    获取count sql
    :param query: sql
    :return:
    """
    count_subquery = typing.cast(typing.Any, query.order_by(None)).options(noload("*")).subquery()
    return select(func.count(literal_column("*"))).select_from(count_subquery)


def paginate_query(query: T, page: int, page_size: int) -> T:
    """
    获取分页sql
    :param query:
    :param page: 页数
    :param page_size: 每页大小
    :return:
    """
    return query.limit(page_size).offset(page_size * (page - 1))


def len_or_none(obj: typing.Any) -> typing.Optional[int]:
    """有数据返回长度 没数据返回None"""
    try:
        return len(obj)
    except TypeError:
        return None


def unwrap_scalars(items: typing.Union[typing.Sequence[Row], Row]) -> typing.Union[
    typing.List[typing.Dict[typing.Text, typing.Any]], typing.Dict[str, typing.Any]]:
    """
    数据库Row对象数据序列化为字典
    :param items: 数据返回数据 [Row(...)]
    :return:
    """
    if isinstance(items, typing.Iterable) and not isinstance(items, Row):
        return [default_serialize(item) for item in items]
    return default_serialize(items)


class MyJsonDecode(JSONEncoder):
    """自定义json解析器"""

    def default(self, obj):
        try:
            return super().default(obj)
        except:
            return default_serialize(obj)


def default_serialize(obj):
    """默认序序列化"""
    try:
        if isinstance(obj, int) and len(str(obj)) > 15:
            return str(obj)
        if isinstance(obj, dict):
            return {key: default_serialize(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [default_serialize(i) for i in obj]
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, Row):
            data = dict(zip(obj._fields, obj._data))
            return {key: default_serialize(value) for key, value in data.items()}
        if hasattr(obj, "__class__") and isinstance(obj.__class__, DeclarativeMeta):
            return {c.name: default_serialize(getattr(obj, c.name)) for c in obj.__table__.columns}
        if isinstance(obj, typing.Callable):
            return repr(obj)
        return jsonable_encoder(obj)
    except TypeError as err:
        return repr(obj)
