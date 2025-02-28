import functools
import sys
from importlib import import_module
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Generic,
    Optional,
    TypeVar,
    Union,
)

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

import anyio
import sniffio
from anyio._core._eventloop import threadlocals
from anyio.abc import TaskGroup as _TaskGroup


# This was obtained with: from anyio._core._eventloop import get_asynclib
# Removed in https://github.com/agronholm/anyio/pull/429
# First release (not released yet): 4.0-dev
def get_asynclib(asynclib_name: Union[str, None] = None) -> Any:
    if asynclib_name is None:
        asynclib_name = sniffio.current_async_library()

    modulename = "anyio._backends._" + asynclib_name
    try:
        return sys.modules[modulename]
    except KeyError:  # pragma: no cover
        return import_module(modulename)


T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")
T = TypeVar("T")


class PendingType:
    def __repr__(self) -> str:
        return "AsyncerPending"


Pending = PendingType()


class PendingValueException(Exception):
    pass


class SoonValue(Generic[T]):
    def __init__(self) -> None:
        self._stored_value: Union[T, PendingType] = Pending

    @property
    def value(self) -> T:
        if isinstance(self._stored_value, PendingType):
            raise PendingValueException(
                "The return value of this task is still pending. Maybe you forgot to "
                "access it after the async with asyncer.create_task_group() block. "
                "If you need to access values of async tasks inside the same task "
                "group, you probably need a different approach, for example with "
                "AnyIO Streams."
            )
        return self._stored_value

    @property
    def ready(self) -> bool:
        return not isinstance(self._stored_value, PendingType)


class TaskGroup(_TaskGroup):
    def soonify(
            self, async_function: Callable[T_ParamSpec, Awaitable[T]], name: object = None
    ) -> Callable[T_ParamSpec, SoonValue[T]]:
        """ """

        @functools.wraps(async_function)
        def wrapper(
                *args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs
        ) -> SoonValue[T]:
            partial_f = functools.partial(async_function, *args, **kwargs)
            soon_value: SoonValue[T] = SoonValue()

            @functools.wraps(partial_f)
            async def value_wrapper() -> None:
                value = await partial_f()
                soon_value._stored_value = value

            self.start_soon(value_wrapper, name=name)
            return soon_value

        return wrapper

    # This is only for the return type annotation, but it won't really be called
    async def __aenter__(self) -> "TaskGroup":  # pragma: nocover
        """Enter the task group context and allow starting new tasks."""
        return await super().__aenter__()  # type: ignore


def create_task_group() -> "TaskGroup":
    """"""

    LibTaskGroup = get_asynclib().TaskGroup

    class ExtendedTaskGroup(LibTaskGroup, TaskGroup):  # type: ignore
        pass

    return ExtendedTaskGroup()


def runnify(
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
        backend: str = "asyncio",
        backend_options: Optional[Dict[str, Any]] = None,
) -> Callable[T_ParamSpec, T_Retval]:
    """"""

    @functools.wraps(async_function)
    def wrapper(*args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs) -> T_Retval:
        partial_f = functools.partial(async_function, *args, **kwargs)

        return anyio.run(partial_f, backend=backend, backend_options=backend_options)

    return wrapper


def async_to_sync(
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
        raise_sync_error: bool = True,
) -> Callable[T_ParamSpec, T_Retval]:
    """
    :param async_function: 异步函数
    :param raise_sync_error: 是否抛出同步错误
    :return:
    """

    @functools.wraps(async_function)
    def wrapper(*args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs) -> T_Retval:
        current_async_module = getattr(threadlocals, "current_async_module", None)
        partial_f = functools.partial(async_function, *args, **kwargs)
        if current_async_module is None and raise_sync_error is False:
            return anyio.run(partial_f)
        return anyio.from_thread.run(partial_f)

    return wrapper


def sync_to_async(
        function: Callable[T_ParamSpec, T_Retval],
        *,
        cancellable: bool = False,
        limiter: Optional[anyio.CapacityLimiter] = None
) -> Callable[T_ParamSpec, Awaitable[T_Retval]]:
    """
    :param function: 同步函数
    :param cancellable: 是否可取消
    :param limiter: 用于限制运行的线程总数的容量限制器 （如果省略，则使用默认限制器）
    :return:
    """

    async def wrapper(
            *args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs
    ) -> T_Retval:
        partial_f = functools.partial(function, *args, **kwargs)
        return await anyio.to_thread.run_sync(
            partial_f, cancellable=cancellable, limiter=limiter
        )

    return wrapper
