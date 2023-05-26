# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from uuid import uuid4

from fastapi import WebSocket
from loguru import logger

from autotest.corelibs import g
from autotest.db.redis import init_redis_pool


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: typing.List[WebSocket] = []
        self.redis = None

    async def init_redis(self):
        self.redis = await init_redis_pool()

    async def connect(self, ws: WebSocket):
        # 等待连接
        g.trace_id = uuid4().hex
        logger.info(f"用户{ws}连接成功")
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        logger.info(f"用户{ws}断开连接")
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


websocket_manager = ConnectionManager()
