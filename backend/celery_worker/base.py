# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import typing


def run_async(func: typing.Union[typing.Coroutine, typing.Awaitable]) -> typing.Any:
    """
    异步函数调用时使用
    :param func:
    :return:
    """
    # 单线程
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func)
    except Exception as err:
        asyncio.set_event_loop(asyncio.new_event_loop())
        return asyncio.run(func)
