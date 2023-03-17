# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import contextvars
import functools
import typing

from starlette.concurrency import run_in_threadpool
from typing_extensions import ParamSpec

T = typing.TypeVar("T")
P = ParamSpec("P")


# def request_response(func: typing.Callable) -> ASGIApp:
#     """
#     Takes a function or coroutine `func(request) -> response`,
#     and returns an ASGI application.
#     """
#     is_coroutine = is_async_callable(func)
#
#     async def app(scope: Scope, receive: Receive, send: Send) -> None:
#         request = Request(scope, receive=receive, send=send)
#         if is_coroutine:
#             response = await func(request)
#         else:
#             response = await run_in_threadpool(func, request)
#         await response(scope, receive, send)
#
#     return app


def async_to_sync(func: typing.Callable, *args: P.args, **kwargs: P.kwargs):
    async def wraps():
        return await run_in_threadpool(func, *args, **kwargs)

    return wraps


class IOLoop:

    @staticmethod
    def async_to_sync(coroutine: typing.Awaitable):
        @functools.wraps
        async def async_handle(*args: P.args, **kwargs: P.kwargs):
            return await run_in_threadpool(coroutine, *args, **kwargs)

        return async_handle

    @staticmethod
    def sync_to_async(func: typing.Callable[P, T]) -> T:
        """同步转异步函数"""

        @functools.wraps(func)
        async def async_handle(*args: P.args, **kwargs: P.kwargs) -> T:
            loop = IOLoop.loop
            if contextvars is not None:
                child = functools.partial(func, *args, **kwargs)
                context = contextvars.copy_context()
                real_func = context.run
                args = (child,)
            elif kwargs:
                real_func = functools.partial(func, **kwargs)
            else:
                real_func = func
            return await loop.run_in_executor(None, real_func, *args)

        return async_handle

    @staticmethod
    async def _await_with_future(coroutine: typing.Awaitable, future: asyncio.Future) -> None:
        """等待执行结果"""
        try:
            result = await coroutine
        except Exception as err:
            future.set_exception(err)
        else:
            future.set_result(result)


#
#
# def sync_to_async(func: typing.Callable[P, T]) -> T:
#     """同步转异步函数"""
#
#     @functools.wraps(func)
#     async def async_handle(*args: P.args, **kwargs: P.kwargs) -> T:
#         loop = asyncio.get_event_loop()
#         if contextvars is not None:
#             child = functools.partial(func, *args, **kwargs)
#             context = contextvars.copy_context()
#             real_func = context.run
#             args = (child,)
#         elif kwargs:
#             real_func = functools.partial(func, **kwargs)
#         else:
#             real_func = func
#         return await loop.run_in_executor(BackgroundTaskExecutor, real_func, *args)
#
#     return async_handle
#
#
# def async_to_sync(coroutine: typing.Awaitable, loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> typing.Any:
#     """异步转同步函数"""
#     new_loop_flag = False
#     if loop is None:
#         try:
#             loop = asyncio.get_event_loop()
#         except RuntimeError:
#             loop = asyncio.new_event_loop()
#             new_loop_flag = True
#
#         result = loop.create_future()
#         asyncio.run(_await_with_future(coroutine, result))
#         if new_loop_flag:
#             # result.done()
#             shutdown_loop(loop=loop)
#         return result.result()
#
#
# def get_loop():
#     try:
#         return asyncio.get_event_loop()
#     except (RuntimeError, AssertionError):
#         return asyncio.new_event_loop()
#
#
# async def _await_with_future(coroutine: typing.Awaitable, future: asyncio.Future) -> None:
#     """等待执行结果"""
#     try:
#         result = await coroutine
#     except Exception as err:
#         future.set_exception(err)
#     else:
#         future.set_result(result)


def all_task(loop: asyncio.AbstractEventLoop = None):
    return asyncio.all_tasks(loop=loop)


def shutdown_loop(loop: asyncio.AbstractEventLoop = None, timeout: float = 1.0):
    tasks = all_task(loop=loop)
    if tasks:
        for task in tasks:
            task.done()
    loop.close()


# def background_task_executor(futures: typing.List[Future]):
#     with ThreadPoolExecutor() as pool:
#         fs = pool.submit(func)
#         return as_completed(fs)


IOLoop = IOLoop()
