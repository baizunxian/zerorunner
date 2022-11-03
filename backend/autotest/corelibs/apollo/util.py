import hashlib
import sys
import socket

version = sys.version_info.major

if version == 3:
    from .python_3x import *

# 定义常量
CONFIGURATIONS = "configurations"
NOTIFICATION_ID = "notificationId"
NAMESPACE_NAME = "namespaceName"


# 对时间戳，uri，秘钥进行加签
def signature(timestamp, uri, secret):
    import hmac
    import base64
    string_to_sign = '' + timestamp + '\n' + uri
    hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(hmac_code).decode()


def url_encode_wrapper(params):
    return url_encode(params)


def no_key_cache_key(namespace, key):
    return "{}{}{}".format(namespace, len(namespace), key)


# 返回是否获取到的值，不存在则返回None
def get_value_from_dict(namespace_cache, key):
    if namespace_cache:
        kv_data = namespace_cache.get(CONFIGURATIONS)
        if kv_data is None:
            return None
        if key in kv_data:
            return kv_data[key]
    return None


def init_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()
    return ""
