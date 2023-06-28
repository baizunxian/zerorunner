# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from loguru import logger

from autotest.apis.websocket.connection_manager import websocket_manager

router = APIRouter()


@router.websocket("/{user}", name="房间")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await websocket_manager.connect(websocket)
    await websocket_manager.init_redis()

    # await websocket_manager.broadcast(f"用户{user}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            try:
                redis_data = await websocket_manager.redis.execute_command(data)
                if isinstance(redis_data, list):
                    redis_data = "\n".join(redis_data)
                # await websocket_manager.send_personal_message(str(redis_data), websocket)
            except Exception as err:
                logger.error(err)
                redis_data = str(err)
            await websocket_manager.send_personal_message(str(redis_data), websocket)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        await websocket_manager.broadcast(f"用户-{user}-离开")

#
# def register_websocket(app: FastAPI):
#     app.add_api_websocket_route("/ws/{user}", websocket_endpoint)
