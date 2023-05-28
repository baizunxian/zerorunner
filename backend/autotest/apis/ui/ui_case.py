# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.corelibs.http_response import partner_success
from autotest.schemas.ui.ui_case import UiCaseQuery, UiCaseId, UiCaseIn
from autotest.services.ui.ui_case import UiCaseServer

router = APIRouter()


@router.post("/list")
async def get_case_list(params: UiCaseQuery):
    """获取用例列表"""
    data = await UiCaseServer.list(params)
    return partner_success(data)


@router.post("/getPageById")
async def get_page_by_id(params: UiCaseId):
    """根据id获取用例信息"""
    data = await UiCaseServer.get_case_by_id(params)
    return partner_success(data)


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
