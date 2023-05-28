# -*- coding: utf-8 -*-
# @author: xiaobai


from fastapi import APIRouter
from autotest.apis.api import project, module, api_info, api_case, test_report, data_source, env, functions, timed_tasks
from autotest.apis.system import user, menu, roles, lookup, id_center, file
from autotest.apis.ui import ui_page, ui_element, ui_case
from autotest.apis.websocket import websocket

app_router = APIRouter()

# api
app_router.include_router(project.router, prefix="/project", tags=["project"])
app_router.include_router(module.router, prefix="/module", tags=["module"])
app_router.include_router(api_info.router, prefix="/apiInfo", tags=["apiInfo"])
app_router.include_router(api_case.router, prefix="/apiCase", tags=["apiCase"])
app_router.include_router(test_report.router, prefix="/report", tags=["testReport"])
app_router.include_router(data_source.router, prefix="/dataSource", tags=["dataSource"])
app_router.include_router(functions.router, prefix="/functions", tags=["functions"])
app_router.include_router(timed_tasks.router, prefix="/timedTasks", tags=["TimedTasks"])
app_router.include_router(env.router, prefix="/env", tags=["env"])

# ui
app_router.include_router(ui_page.router, prefix="/uiPage", tags=["uiPage"])
app_router.include_router(ui_element.router, prefix="/uiElement", tags=["uiElement"])
app_router.include_router(ui_case.router, prefix="/uiCase", tags=["uiCase"])

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(menu.router, prefix="/menu", tags=["menu"])
app_router.include_router(roles.router, prefix="/roles", tags=["roles"])
app_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
app_router.include_router(id_center.router, prefix="/idCenter", tags=["idCenter"])
app_router.include_router(file.router, prefix="/file", tags=["file"])

# websocket
app_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
