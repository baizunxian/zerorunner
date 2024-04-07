# -*- coding: utf-8 -*-
# @author: xiao bai

import json
import pickle
import typing

from aioredis import Redis, DataError
from redis import Redis as SyncRedis
from redis.typing import KeyT, FieldT, EncodableT, AnyFieldT

from config import config


class MyAsyncRedis(Redis):
    """ 异步Redis,并添加自己的方法 """

    # 写 __init__ 的话就取消下面注释
    # def __init__(self, connection_pool):
    #     # print(connection_pool)
    #     super(RedisPlus, self).__init__(connection_pool=connection_pool)
    async def get(self, name: str) -> typing.Any:
        data = await super(MyAsyncRedis, self).get(name)
        return json.loads(data) if data else None

    async def set(
            self,
            name: str,
            value: typing.Any,
            ex: typing.Optional[int] = None,
    ) -> typing.Any:
        return await super(MyAsyncRedis, self).set(name, json.dumps(value), ex=ex)

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

    async def cus_lpush_by_pickle(self, key: str, value: typing.Union[str, list, dict]):
        """
        向列表右侧插入数据
        :param key: 列表的key
        :param value: 插入的值
        """
        text = pickle.dumps(value)
        await self.lpush(key, text)

    async def cus_lpop_by_pickle(self, key: str):
        """
        获取list数据
        :param key: 列表的key
        """
        r = await self.lpop(key)
        if r:
            return pickle.loads(r)
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


class MySyncRedis(SyncRedis):
    """同步redis"""

    def get(self, name: str) -> typing.Any:
        data = super(MySyncRedis, self).get(name)
        return json.loads(data) if data else None


class RedisPool:
    _redis: MyAsyncRedis = None

    @property
    def redis(self):
        return self._redis

    def init_by_config(self, config):
        if self.redis:
            return self.redis
        if not hasattr(config, "REDIS_URI"):
            raise Exception("配置REDIS_URL不能为空！~")
        return self._form_url(config.REDIS_URI)

    def _form_url(self, url: str):
        if not url:
            raise Exception("配置REDIS_URL不能为空！~")
        try:
            self._redis = MyAsyncRedis.from_url(url=url, health_check_interval=30)
            return self.redis
        except Exception as e:
            raise Exception(f"连接redis失败: {e}")

    def get_redis(self):
        if not self.redis:
            raise Exception("请先初始化redis连接池！~, 请调用init_app或init_by_config方法")
        return self.redis


redis_pool = RedisPool()
redis_pool.init_by_config(config=config)
