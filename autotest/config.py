import json
import os
import socket
import traceback

from flask_sqlalchemy import SQLAlchemy
from loguru import logger

db = SQLAlchemy(session_options={"autoflush": False, "autocommit": False, "expire_on_commit": False})


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as err:
        logger.error(traceback.format_exc())
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip


SERVER_IP = get_host_ip()
PRD_IP = '127.0.0.2'
DEV_ID = '127.0.0.1'

if SERVER_IP == PRD_IP:
    from autotest.config_dev import CONFIGS
else:
    from autotest.config_dev import CONFIGS


def _get_from_env(name, default=None):
    """
    从环境变量中获取配置

    :param name: 配置名，可以使用小写字母，会自动转成大写
    :param default: 当变量不存在时候使用的默认值
    """
    raw_value = os.environ.get(name, default)
    if raw_value is not None:
        try:
            return json.loads(raw_value)
        except (ValueError, TypeError):
            return raw_value


class Config:
    """
    Config 类

    从系统环境变量中获取配置信息。
    """

    def __init__(self, update=None):
        # copy
        conf = CONFIGS
        self._default_configs = {k: v for k, v in conf.items()}
        if update:
            self.update(update)

    def update(self, update):
        """更新默认信息"""
        self._default_configs.update(update)

    def iteritems(self):
        """iteritems"""
        return iter([(k, self.__getattr__(k))
                     for k, _ in self._default_configs.items()])

    def __getattr__(self, name):
        # name = name.upper()
        default = self._default_configs.get(name, None)
        value = _get_from_env(name, default=default)
        return value


config = Config()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s | %(levelname)s | %(thread)d | %(name)s | %(message)s',
        },
        'file_format': {
            'format': '%(asctime)s | %(levelname)s | %(thread)d | %(name)s | %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_format',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'DEBUG',
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 10,
            # 最多保留100份文件
            'backupCount': 10,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            # 'filename': '/app/logs/autotest_backend.log',
            'filename': '/app/logs/autotest_backend.log' if SERVER_IP == PRD_IP else 'logs/autotest_backend.log',
            'formatter': 'file_format'
        }
    },
    'loggers': {
        'file': {
            'level': 'INFO',
            'handlers': ['file'] if SERVER_IP == PRD_IP else ['console'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file'] if SERVER_IP == PRD_IP else ['console'],
    },
}
