# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from uuid import uuid4

from fastapi import WebSocket
from loguru import logger

from autotest.db.my_redis import redis_pool
from autotest.utils.local import g


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: typing.List[WebSocket] = []
        self.redis = None

    async def init_redis(self):
        self.redis = redis_pool.redis

    async def connect(self, ws: WebSocket):
        # 等待连接
        g.trace_id = uuid4().hex
        logger.info(f"{ws}连接成功")
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        logger.info(f"{ws}断开连接")
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    @staticmethod
    async def send_personal_message_json(message: typing.Any, ws: WebSocket):
        # 发送个人消息  json 格式
        await ws.send_json(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


websocket_manager = ConnectionManager()
