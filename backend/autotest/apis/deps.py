# -*- coding: utf-8 -*-
# @author: xiaobai


import typing

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from autotest.config.config import config
from autotest.db.redis import MyRedis
from autotest.db.session import async_session

get_token = OAuth2PasswordBearer(tokenUrl=f"{config.API_PREFIX}/login")


async def get_db() -> typing.AsyncGenerator[AsyncSession, None]:
    """ sql连接会话 """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis(request: Request) -> MyRedis:
    """ redis连接对象 """
    return await request.app.state.redis
