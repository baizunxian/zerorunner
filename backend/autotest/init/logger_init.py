# -*- coding: utf-8 -*-
# @author: xiaobai
import os
import sys
import logging
from loguru import logger

from config import config
from autotest.utils.local import g
from autotest.utils.create_dir import create_dir

# 创建日志文件名
from autotest.utils.common import get_str_uuid


def logger_file() -> str:
    """ 创建日志文件名 """
    log_path = create_dir(config.LOGGER_DIR)

    """ 保留日志文件夹下最大个数(本地调试用) 
    本地调式需要多次重启, 日志轮转片不会生效 """
    file_list = os.listdir(log_path)
    if len(file_list) > 3:
        os.remove(os.path.join(log_path, file_list[0]))

    # 日志输出路径
    return os.path.join(log_path, config.LOGGER_NAME)


def correlation_id_filter(record):
    if not g.trace_id:
        g.trace_id = get_str_uuid()
    record['trace_id'] = g.trace_id
    return record


# 详见: https://loguru.readthedocs.io/en/stable/overview.html#features
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>| {thread} | <level>{level: <8}</level> | <yellow> {trace_id} </yellow> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
logger.remove()
logger.add(
    # logger_file(),
    sys.stdout,
    # encoding=config.GLOBAL_ENCODING,
    level=config.LOGGER_LEVEL,
    colorize=True,
    # rotation=config.LOGGER_ROTATION,
    # retention=config.LOGGER_RETENTION,
    filter=correlation_id_filter,
    format=fmt,
    # enqueue=True
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(level, record.getMessage())


def init_logger():
    logger_name_list = [name for name in logging.root.manager.loggerDict]

    for logger_name in logger_name_list:
        """获取所有logger"""
        effective_level = logging.getLogger(logger_name).getEffectiveLevel()
        if effective_level < logging.getLevelName(config.LOGGER_LEVEL.upper()):
            logging.getLogger(logger_name).setLevel(config.LOGGER_LEVEL.upper())
        if '.' not in logger_name:
            logging.getLogger(logger_name).handlers = []
            logging.getLogger(logger_name).addHandler(InterceptHandler())
