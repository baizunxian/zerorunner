# -*- coding: utf-8 -*-
# @author: xiao bai
import typing

from fastapi import FastAPI

from autotest.db.my_redis import MyAsyncRedis
from config import config

ZRedis = None


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_async_redis_pool(app: typing.Optional[FastAPI] = None) -> MyAsyncRedis:
    """ 连接redis """
    global ZRedis
    redis = await MyAsyncRedis.from_url(url=config.REDIS_URI,
                                        # encoding=config.GLOBAL_ENCODING,
                                        # decode_responses=True,
                                        health_check_interval=30)
    ZRedis = redis
    if app is not None:
        app.state.redis = redis
    return redis
