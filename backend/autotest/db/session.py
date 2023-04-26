# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import traceback
from asyncio import current_task
import functools
import typing

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from autotest.config.config import config

# 创建表引擎
from loguru import logger

# # 操作表会话
# async_session = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     autoflush=False,
#     autocommit=False,
#     expire_on_commit=False  # 防止提交后属性过期
# )


engine = create_async_engine(
    url=config.DATABASE_URI,  # 数据库uri
    echo=config.DATABASE_ECHO,  # 是否打印日志
    pool_size=10,  # 队列池个数
    max_overflow=20,  # 队列池最大溢出个数
    pool_pre_ping=False
)

# 操作表会话
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # 防止提交后属性过期
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)


def provide_session(func: typing.Callable):
    """
    :param func: 函数
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        arg_session = 'session'

        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs

        if session_in_kwargs or session_in_args:
            return await func(*args, **kwargs)
        else:
            async with async_session() as session:
                fs = functools.partial(func, session=session, *args, **kwargs)
                try:
                    return await fs()
                except IntegrityError:
                    logger.error(traceback.format_exc())
                    await session.rollback()
                    raise
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.commit()
                    await async_session.remove()

    return wrapper
