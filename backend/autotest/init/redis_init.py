# -*- coding: utf-8 -*-
# @author: xiao bai
from autotest.db.my_redis import MyRedis
from config import config


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> MyRedis:
    """ 连接redis """
    redis = await MyRedis.from_url(url=config.REDIS_URI,
                                   encoding=config.GLOBAL_ENCODING,
                                   decode_responses=True,
                                   health_check_interval=30)
    return redis
