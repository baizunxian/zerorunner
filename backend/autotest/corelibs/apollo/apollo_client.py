import json
import threading
import time

from .util import *

version = sys.version_info.major

if version == 3:
    from .python_3x import *

# logging.basicConfig()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)


class ApolloClient(object):

    def __init__(self, config_url, app_id, cluster='default', secret='', start_hot_update=False,
                 change_listener=None):

        # 核心路由参数
        self.config_url = config_url
        self.cluster = cluster
        self.app_id = app_id

        # 非核心参数
        self.ip = init_ip()
        self.secret = secret

        # 检查参数变量

        # 私有控制变量
        self._cycle_time = 2
        self._stopping = True
        self._cache = {}
        self._no_key = {}
        self._hash = {}
        self._pull_timeout = 75
        self._cache_file_path = '/app/apollo/cache/'
        self._long_poll_thread = None
        self._change_listener = change_listener  # "add" "delete" "update"

        # 私有启动方法
        self._path_checker()
        if start_hot_update:
            self._start_hot_update()

        # 启动心跳线程
        heartbeat = threading.Thread(target=self._heartBeat)
        heartbeat.setDaemon(True)
        heartbeat.start()

    def get_json_from_net(self, namespace='application'):
        url = '{}/configs/{}/{}/{}?releaseKey={}&ip={}'.format(self.config_url, self.app_id, self.cluster, namespace,
                                                               "", self.ip)
        try:
            code, body = http_request(url, timeout=3, headers=self._signHeaders(url))
            if code == 200:
                data = json.loads(body)
                data = data["configurations"]
                return_data = {CONFIGURATIONS: data}
                return return_data
            else:
                return None
        except Exception as e:
            logging.getLogger(__name__).error(str(e))
            return None

    def get_value(self, key, default_val=None, namespace='application'):
        try:
            # 读取内存配置
            namespace_cache = self._cache.get(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                return val

            no_key = no_key_cache_key(namespace, key)
            if no_key in self._no_key:
                return default_val

            # 读取网络配置
            namespace_data = self.get_json_from_net(namespace)
            val = get_value_from_dict(namespace_data, key)
            if val is not None:
                self._update_cache_and_file(namespace_data, namespace)
                return val

            # 读取文件配置
            namespace_cache = self._get_local_cache(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                self._update_cache_and_file(namespace_cache, namespace)
                return val

            # 如果全部没有获取，则把默认值返回，设置本地缓存为None
            self._set_local_cache_none(namespace, key)
            return default_val
        except Exception as e:
            logging.getLogger(__name__).error("get_value has error, [key is %s], [namespace is %s], [error is %s], ",
                                              key, namespace, e)
            return default_val

    # 设置某个namespace的key为none，这里不设置default_val，是为了保证函数调用实时的正确性。
    # 假设用户2次default_val不一样，然而这里却用default_val填充，则可能会有问题。
    def _set_local_cache_none(self, namespace, key):
        no_key = no_key_cache_key(namespace, key)
        self._no_key[no_key] = key

    def _start_hot_update(self):
        self._long_poll_thread = threading.Thread(target=self._listener)
        # 启动异步线程为守护线程，主线程推出的时候，守护线程会自动退出。
        self._long_poll_thread.setDaemon(True)
        self._long_poll_thread.start()

    def stop(self):
        self._stopping = True
        logging.getLogger(__name__).info("Stopping listener...")

    # 调用设置的回调函数，如果异常，直接try掉
    def _call_listener(self, namespace, old_kv, new_kv):
        if self._change_listener is None:
            return
        if old_kv is None:
            old_kv = {}
        if new_kv is None:
            new_kv = {}
        try:
            for key in old_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if new_value is None:
                    # 如果newValue 是空，则表示key，value被删除了。
                    self._change_listener("delete", namespace, key, old_value)
                    continue
                if new_value != old_value:
                    self._change_listener("update", namespace, key, new_value)
                    continue
            for key in new_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if old_value is None:
                    self._change_listener("add", namespace, key, new_value)
        except BaseException as e:
            logging.getLogger(__name__).warning(str(e))

    def _path_checker(self):
        if not os.path.isdir(self._cache_file_path):
            makedirs_wrapper(self._cache_file_path)

    # 更新本地缓存和文件缓存
    def _update_cache_and_file(self, namespace_data, namespace='application'):
        # 更新本地缓存
        self._cache[namespace] = namespace_data
        # 更新文件缓存
        new_string = json.dumps(namespace_data)
        new_hash = hashlib.md5(new_string.encode('utf-8')).hexdigest()
        if self._hash.get(namespace) == new_hash:
            pass
        else:
            with open(os.path.join(self._cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace)),
                      'w') as f:
                f.write(new_string)
            self._hash[namespace] = new_hash

    # 从本地文件获取配置
    def _get_local_cache(self, namespace='application'):
        cache_file_path = os.path.join(self._cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace))
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, 'r') as f:
                result = json.loads(f.readline())
            return result
        return {}

    def _long_poll(self):
        notifications = []
        for key in self._cache:
            namespace_data = self._cache[key]
            notification_id = -1
            if NOTIFICATION_ID in namespace_data:
                notification_id = self._cache[key][NOTIFICATION_ID]
            notifications.append({
                NAMESPACE_NAME: key,
                NOTIFICATION_ID: notification_id
            })
        try:
            # 如果长度为0直接返回
            if len(notifications) == 0:
                return
            url = '{}/notifications/v2'.format(self.config_url)
            params = {
                'appId': self.app_id,
                'cluster': self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }
            param_str = url_encode_wrapper(params)
            url = url + '?' + param_str
            code, body = http_request(url, self._pull_timeout, headers=self._signHeaders(url))
            http_code = code
            if http_code == 304:
                logging.getLogger(__name__).debug('No change, loop...')
                return
            if http_code == 200:
                data = json.loads(body)
                for entry in data:
                    namespace = entry[NAMESPACE_NAME]
                    n_id = entry[NOTIFICATION_ID]
                    logging.getLogger(__name__).info("%s has changes: notificationId=%d", namespace, n_id)
                    self._get_net_and_set_local(namespace, n_id, call_change=True)
                    return
            else:
                logging.getLogger(__name__).warning('Sleep...')
        except Exception as e:
            logging.getLogger(__name__).warning(str(e))

    def _get_net_and_set_local(self, namespace, n_id, call_change=False):
        namespace_data = self.get_json_from_net(namespace)
        namespace_data[NOTIFICATION_ID] = n_id
        old_namespace = self._cache.get(namespace)
        self._update_cache_and_file(namespace_data, namespace)
        if self._change_listener is not None and call_change:
            old_kv = old_namespace.get(CONFIGURATIONS)
            new_kv = namespace_data.get(CONFIGURATIONS)
            self._call_listener(namespace, old_kv, new_kv)

    def _listener(self):
        logging.getLogger(__name__).info('start long_poll')
        while not self._stopping:
            self._long_poll()
            time.sleep(self._cycle_time)
        logging.getLogger(__name__).info("stopped, long_poll")

    # 给header增加加签需求
    def _signHeaders(self, url):
        headers = {}
        if self.secret == '':
            return headers
        uri = url[len(self.config_url):len(url)]
        time_unix_now = str(int(round(time.time() * 1000)))
        headers['Authorization'] = 'Apollo ' + self.app_id + ':' + signature(time_unix_now, uri, self.secret)
        headers['Timestamp'] = time_unix_now
        return headers

    def _heartBeat(self):
        while not self._stopping:
            time.sleep(60 * 10)  # 10分钟
            for namespace in self._notification_map:
                self._do_heartBeat(namespace)

    def _do_heartBeat(self, namespace):
        release_key = self._release_key_map.get(namespace)
        url = '{}/configs/{}/{}/{}?releaseKey={}&ip={}'.format(self.config_url, self.app_id, self.cluster, namespace,
                                                               release_key, self.ip)
        try:
            code, body = http_request(url, timeout=3, headers=self._signHeaders(url))
            if code == 200:
                data = json.loads(body)
                self._release_key_map[namespace] = data["releaseKey"]
                data = data["configurations"]
                self._update_cache_and_file(data, namespace)
            else:
                return None
        except Exception as e:
            logging.getLogger(__name__).error(str(e))
            return None
