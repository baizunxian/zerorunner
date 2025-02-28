# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.ui.ui_case import UiCaseQuery, UiCaseId, UiCaseIn, UiTestCaseRun
from autotest.services.ui.ui_case import UiCaseServer
from autotest.utils.current_user import current_user
from celery_worker.tasks.ui_case import async_run_ui

router = APIRouter()


@router.post("/list", description="获取ui用例列表")
async def get_case_list(params: UiCaseQuery):
    """获取用例列表"""
    data = await UiCaseServer.list(params)
    return partner_success(data)


@router.post("/getUiCaseById", description="更具id获取ui用例")
async def get_ui_case_by_id(params: UiCaseId):
    """根据id获取用例信息"""
    data = await UiCaseServer.get_case_by_id(params)
    return partner_success(data)


@router.post("/runUiCaseById")
async def run_ui_case_by_id(params: UiTestCaseRun):
    """根据id运行ui用例信息"""
    if not params.id:
        raise ValueError("id 不能为空！")
    current_user_info = await current_user()
    exec_user_id = current_user_info.get("id", None)
    exec_user_name = current_user_info.get("nickname", None)
    kwargs = dict(ui_id=params.id,
                  env_id=params.env_id,
                  exec_user_id=exec_user_id,
                  exec_user_name=exec_user_name)
    async_run_ui.apply_async(kwargs=kwargs, __business_id=params.id)
    # await async_run_ui(**kwargs)

    return partner_success(msg="用例异步运行， 请稍后再测试报告列表查看 😊")


@router.post("/saveOrUpdate")
async def save_or_update(params: UiCaseIn):
    """保存或更新用例信息"""
    data = await UiCaseServer.save_or_update(params)
    return partner_success(data)


@router.post("/deleted")
async def deleted(params: UiCaseIn):
    """删除用例信息"""
    data = await UiCaseServer.deleted(params.id)
    return partner_success(data)
