# -*- coding: utf-8 -*-
# @author: xiaobai


import json
import typing
from aioredis import Redis, DataError
from redis.typing import KeyT, FieldT, EncodableT, AnyFieldT

from config import config


class MyRedis(Redis):
    """ 继承Redis,并添加自己的方法 """

    # 写 __init__ 的话就取消下面注释
    # def __init__(self, connection_pool):
    #     # print(connection_pool)
    #     super(RedisPlus, self).__init__(connection_pool=connection_pool)
    async def get(self, name: str) -> typing.Any:
        data = await super(MyRedis, self).get(name)
        return json.loads(data) if data else None

    async def set(
            self,
            name: str,
            value: typing.Any,
            ex: typing.Optional[int] = None,
    ) -> typing.Any:
        return await super(MyRedis, self).set(name, json.dumps(value), ex=ex)

    async def list_loads(self, key: str, num: int = -1) -> list:
        """
        将列表字符串转为对象
        :param key: 列表的key
        :param num: 最大长度(默认值 0-全部)
        :return: 列表对象
        """
        todo_list = await self.lrange(key, 0, (num - 1) if num > -1 else num)
        return [json.loads(todo) for todo in todo_list]

    async def cus_lpush(self, key: str, value: typing.Union[str, list, dict]):
        """
        向列表右侧插入数据
        :param key: 列表的key
        :param value: 插入的值
        """
        text = json.dumps(value)
        await self.lpush(key, text)

    async def cus_lpop(self, key: str):
        """
        获取list数据
        :param key: 列表的key
        """
        r = await self.lpop(key)
        if r:
            return json.loads(r)
        return None

    async def hset(
            self,
            name: KeyT,
            key: typing.Optional[FieldT] = None,
            value: typing.Optional[EncodableT] = None,
            mapping: typing.Optional[typing.Mapping[AnyFieldT, EncodableT]] = None,
    ) -> typing.Awaitable:

        if key is None and not mapping:
            raise DataError("'hset' with no key value pairs")
        items: typing.List[typing.Union[FieldT, typing.Optional[EncodableT]]] = []
        if key is not None:
            items.extend((key, json.dumps(value)))
        if mapping:
            for pair in mapping.items():
                items.extend(pair)

        return self.execute_command("HSET", name, *items)

    async def get_list_by_index(self, key: str, id: int) -> object:
        """
        根据索引得到列表值
        :param key: 列表的值
        :param id: 索引值
        :return:
        """
        value = await self.lindex(key, id)
        return json.loads(value)


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> MyRedis:
    """ 连接redis """
    redis = await MyRedis.from_url(url=config.REDIS_URI, encoding=config.GLOBAL_ENCODING, decode_responses=True)
    return redis
