import _pickle as cPickle
import redis

try:
    import simplejson as json
except ImportError:
    import json

# _CACHE_KEY_PREFIX = "test:"  # redis 生产的key 必须也这个定义的开头
_CACHE_KEY_PREFIX = ""  # redis 生产的key 必须也这个定义的开头


def require_prefix(f):  # 校验key是否已_CACHE_KEY_PREFIX 定义的值开头
    def func(self, key, *args, **kws):
        if not key.startswith(_CACHE_KEY_PREFIX):
            raise KeyError('%s is not starts with %s'.format(key, _CACHE_KEY_PREFIX))
        return f(self, key, *args, **kws)

    return func


class BRedis:  # redis 封装类 (名字随意)

    def __init__(self, app=None):  # 初始化redis 类
        self._client = None

        if app is not None:
            self.init_app(app)

    def __getattr__(self, name):
        return getattr(self._client, name)

    def init_app(self, app):  # 初始化redis 配置
        uri = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        max_conn = app.config.get('REDIS_MAX_CONNECTIONS', 1024)
        self._client = redis.StrictRedis.from_url(uri, max_connections=max_conn)

        if not hasattr(app, 'extensions'):  # 判断app是否有扩展否则的话添加
            app.extensions = {}
        app.extensions['br'] = self

    def get(self, key):  # redis get 方法封装
        r = self._client.get(key)
        if r:
            return json.loads(r)
        else:
            return None

    def exists(self, key):  # redis exists 方法封装
        r = self._client.exists(key)
        if r:
            return True
        else:
            return False

    @require_prefix
    def set(self, key, value, expire=0, compress=False):
        if value is None:
            return None
        # todo: 如果以后要优化，value可以压缩, 暂时compress那个参数没有使用
        v = json.dumps(value)
        if expire:
            return self._client.setex(key, expire, v)
        else:
            return self._client.set(key, v)

    @require_prefix
    def incr(self, key):
        return self._client.incrby(key)

    @require_prefix
    def db_set(self, key, value, expire=0, compress=False):
        """只提供给sqlalchemy python中使用"""
        if value is None:
            return None
        # todo: 如果以后要优化，value可以压缩, 暂时compress那个参数没有使用
        v = cPickle.dumps(value)
        if expire:
            return self._client.setex(key, expire, v)
        else:
            return self._client.set(key, v)

    def db_get(self, key):
        r = self._client.get(key)
        if r:
            return cPickle.loads(r)
        else:
            return None

    @require_prefix
    def add(self, key, value, expire=0):
        if value is None and expire > 0:
            self._client.expire(key, expire)
            return self.get(key)

        if value:
            r = self._client.incrby(key, value)
            if expire:
                self._client.expire(key, expire)
            return r

    @require_prefix
    def lpush(self, name, *values):
        v = json.dumps(*values)
        return self._client.lpush(name, v)

    @require_prefix
    def rpush(self, name, *values):
        v = json.dumps(*values)
        return self._client.rpush(name, v)

    @require_prefix
    def lpop(self, name):
        r = self._client.lpop(name)
        if r:
            return json.loads(r)
        return None

    @require_prefix
    def rpop(self, name):
        r = self._client.rpop(name)
        if r:
            return json.loads(r)
        return None

    @require_prefix
    def llen(self, name):
        return self._client.llen(name)

    @require_prefix
    def lrange(self, name, start, end):
        return self._client.lrange(name, start, end)

    @require_prefix
    def lrem(self, name, count, value):
        return self._client.lrem(name, count, value)

    @require_prefix
    def hset(self, key, field, value):
        v = json.dumps(value)
        return self._client.hset(key, field, v)

    @require_prefix
    def hget(self, key, field):
        r = self._client.hget(key, field)
        if r:
            return json.loads(r)
        return None

    def expire(self, key, expire=0):
        """
        设置过期时间
        :param key:
        :param expire:
        :return:
        """
        return self._client.expire(key, expire)

    @require_prefix
    def hincrby(self, key, field, number_value):
        """为整型值增加指定的增量，可以指定增量为负数实现减量"""
        return self._client.hincrby(key, field, number_value)

    @require_prefix
    def hexists(self, key, field):
        """
        field 存在，返回 1。
        field 不存在，返回 0。
        :param key:
        :param field:
        :return:
        """
        return self._client.hexists(key, field)

    @require_prefix
    def lrem(self, name, count, value):
        return self._client.lrem(name, count, value)

    def delete(self, *keys):
        if len(keys) < 1:
            return
        return self._client.delete(*keys)

    def flushdb(self):
        self._client.flushdb()

    @require_prefix
    def delete_pattern(self, pattern, batch_size=2000):
        """
        This method uses Redis's `scan` command to delete all
        keys with given pattern instead of using `keys` command (which
        may introduce performance issues, see http://redis.io/commands/keys).

        Internally this method repeatedly call `scan` until the whole
        collection is scanned.

        This method is not atomic, you should not use this if atomicity is
        vital. (for general cases this method should be ok).

        If the size of database is growing fast enough, this method may never
        terminate. (depends on the `batch_size` parameter and the
        speed of growth)

        :param str pattern: pattern to delete
        :param int batch_size: the batch size to examine, passed to redis as
            `count` parameter.
        """
        cursor = 0
        while True:
            cursor, keys = self.scan(cursor, match=pattern, count=batch_size)
            self.delete(*keys)
            if cursor == 0:
                break

    @require_prefix
    def get_keys_by_pattern(self, pattern, max_num=1000, batch_size=2000):
        """从 Redis 中获取满足某个 pattern 的 key。
        支持的 pattern 跟 redis keys 命令一样。

        :param str pattern: 要匹配的 pattern
        :param int max_num: 最多获取多少个 key
        :param int batch_size: 每次遍历的 key 的数量，不满足 pattern 的 key 也会计算，因此 \
            每次实际返回的 key 的数量会小于等于 batch_size
        :return: 返回一个匹配的 key 的迭代器
        """
        cursor = 0
        count = 0
        while True:
            cursor, result = self.scan(cursor, match=pattern, count=batch_size)
            count += len(result)
            for key in result:
                yield key
            if count >= max_num:
                return
            if cursor == 0:
                return


br = BRedis()
