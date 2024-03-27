# -*- coding: utf-8 -*-
# @author: xiaobai
import functools
import traceback
import typing
from asyncio import current_task
from contextvars import ContextVar

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from autotest.utils.local import g
from config import config

SQLAlchemySession: ContextVar[typing.Optional[AsyncSession]] = ContextVar('SQLAlchemySession', default=None)


# 创建表引擎

async_engine = create_async_engine(
    url=config.DATABASE_URI,  # 数据库uri
    echo=config.DATABASE_ECHO,  # 是否打印日志
    pool_size=10,  # 队列池个数
    max_overflow=20,  # 队列池最大溢出个数
    pool_pre_ping=True,  # 将启用连接池“预ping”功能，该功能在每次签出时测试连接的活跃度
    pool_recycle=7200,  # 2个小时回收线程
)

# 操作表会话
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # 防止提交后属性过期
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

sync_engine = create_engine(
    url=config.DATABASE_URI,  # 数据库uri
    echo=config.DATABASE_ECHO,  # 是否打印日志
    pool_size=10,  # 队列池个数
    max_overflow=20,  # 队列池最大溢出个数
    pool_pre_ping=True,  # 将启用连接池“预ping”功能，该功能在每次签出时测试连接的活跃度
    pool_recycle=7200,  # 2个小时回收线程
)
sync_session = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False, expire_on_commit=False)


def provide_async_session(func: typing.Callable):
    """
    单事务回滚
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
                    logger.error(traceback.format_exc())
                    await session.rollback()
                    raise
                finally:
                    await session.commit()
                    await async_session.remove()

    return wrapper


def provide_async_session_router(func: typing.Callable):
    """
    路由全局错误回滚
    :param func: 函数
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            g.zero_db_session = session
            try:
                return await func(*args, **kwargs)
            except IntegrityError:
                await session.rollback()
                logger.error(traceback.format_exc())
                raise
            except Exception:
                await session.rollback()
                logger.error(traceback.format_exc())
                raise
            finally:
                await session.commit()
                await async_session.remove()

    return wrapper

