# -*- coding: utf-8 -*-
# @author: xiaobai
import json

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from loguru import logger

from autotest.apis.websocket.connection_manager import websocket_manager
from autotest.schemas.ui.ui_case import UiDebugCaseIn
from autotest.services.ui.ui_case import UiCaseServer
from zerorunner.ext.zero_driver.driver import DriverSetting, ZeroDriver
from zerorunner.models.result_model import StepResult
from zerorunner.models.step_model import TConfig
from zerorunner.runner import SessionRunner

router = APIRouter()

driver_app_obj = {}


@router.websocket("/debug/{id}", name="调试ui用例")
async def websocket_endpoint(websocket: WebSocket, id: str):
    await websocket_manager.connect(websocket)
    await websocket_manager.init_redis()

    # await websocket_manager.broadcast(f"用户{user}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            try:
                new_data = UiDebugCaseIn.parse_obj(json.loads(data))
                ui_case_info = await UiCaseServer.handel_ui_case2run_schemas(new_data.data)
                if id not in driver_app_obj:
                    driver_setting = DriverSetting(
                        command_executor="http://xiaobaicodes.com:4444/wd/hub",
                        headless=False
                    )
                    driver_app = ZeroDriver(driver_setting)
                    driver_app_obj[id] = driver_app

                if ui_case_info.teststeps:
                    for index, step in enumerate(ui_case_info.teststeps):
                        try:
                            runner = SessionRunner()
                            runner.config = TConfig(
                                name="test",
                            )
                            runner.zero_driver = driver_app_obj[id]
                            runner.run_step(step)
                            step_result = runner.get_step_results()[0] if runner.get_step_results() else StepResult(
                                index=step.struct().index,
                                name=step.name,)
                            send_data = {
                                "message_type": "step_result",
                                "step_result": step_result.dict(),
                            }
                            await websocket_manager.send_personal_message_json(send_data, websocket)
                        except Exception as err:
                            logger.error(err)
                            step_result = StepResult(
                                index=step.struct().index,
                                name=step.name,
                                log=f"执行错误 {err}",
                            )
                            send_data = {
                                "message_type": "step_result",
                                "step_result": step_result.dict(),
                            }
                            await websocket_manager.send_personal_message_json(send_data, websocket)
                            break
            except Exception as err:
                logger.error(err)
                log_data = {
                    "message_type": "err",
                    "data": f"执行错误 {err}",
                }
                await websocket_manager.send_personal_message_json(log_data, websocket)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        driver_app_obj[id].quit()
        await websocket_manager.broadcast(f"用户-{id}-离开")
