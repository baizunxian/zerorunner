# -*- coding: utf-8 -*-
# @author: xiaobai


from fastapi import APIRouter
from autotest.apis.api import (
    project,
    module,
    api_info,
    api_case,
    api_report,
    data_source,
    env,
    functions,
    timed_tasks,
    relation_graph
)
from autotest.apis.system import user, menu, roles, lookup, id_center, file, statistics
from autotest.apis.ui import ui_page, ui_element, ui_case, ui_report
from autotest.apis.coverage import coverage_report, repository_manager
from autotest.apis.websocket import websocket
from autotest.apis.websocket.ui import web_ui_case
from autotest.apis.job import task_record

app_router = APIRouter()

# api
app_router.include_router(project.router, prefix="/project", tags=["project"])
app_router.include_router(module.router, prefix="/module", tags=["module"])
app_router.include_router(api_info.router, prefix="/apiInfo", tags=["apiInfo"])
app_router.include_router(api_case.router, prefix="/apiCase", tags=["apiCase"])
app_router.include_router(api_report.router, prefix="/report", tags=["apiReport"])
app_router.include_router(data_source.router, prefix="/dataSource", tags=["dataSource"])
app_router.include_router(functions.router, prefix="/functions", tags=["functions"])
app_router.include_router(timed_tasks.router, prefix="/timedTasks", tags=["TimedTasks"])
app_router.include_router(env.router, prefix="/env", tags=["env"])
app_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
app_router.include_router(relation_graph.router, prefix="/relationGraph", tags=["relationGraph"])

# ui
app_router.include_router(ui_page.router, prefix="/uiPage", tags=["uiPage"])
app_router.include_router(ui_element.router, prefix="/uiElement", tags=["uiElement"])
app_router.include_router(ui_case.router, prefix="/uiCase", tags=["uiCase"])
app_router.include_router(ui_report.router, prefix="/uiReport", tags=["uiReport"])

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(menu.router, prefix="/menu", tags=["menu"])
app_router.include_router(roles.router, prefix="/roles", tags=["roles"])
app_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
app_router.include_router(id_center.router, prefix="/idCenter", tags=["idCenter"])
app_router.include_router(file.router, prefix="/file", tags=["file"])

# coverage
app_router.include_router(coverage_report.router, prefix="/coverage/report", tags=["coverage"])
app_router.include_router(repository_manager.router, prefix="/coverage/repository", tags=["repository"])

# job
app_router.include_router(task_record.router, prefix="/job", tags=["job"])

# websocket
app_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
app_router.include_router(web_ui_case.router, prefix="/ws/uiCase", tags=["UIWebsocket"])
