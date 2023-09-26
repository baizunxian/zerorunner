# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId
from autotest.services.ui.ui_page import UiPageServer

router = APIRouter()


@router.post("/list", description="获取页面列表")
async def ui_page_list(params: UiPageQuery):
    """获取页面列表"""
    data = await UiPageServer.list(params)
    return partner_success(data)


@router.post("/getPageById", description="根据id获取页面信息")
async def get_page_by_id(params: UiPageId):
    """根据id获取页面信息"""
    data = await UiPageServer.get_page_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新页面信息")
async def save_or_update(params: UiPageIn):
    """保存或更新页面信息"""
    data = await UiPageServer.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除页面信息")
async def deleted(params: UiPageId):
    """删除页面信息"""
    data = await UiPageServer.deleted(params.id)
    return partner_success(data)


@router.post("/getAllPageElement", description="获取页面元素信息")
async def get_all_page_element():
    """获取页面元素信息"""
    data = await UiPageServer.get_all_page_element()
    return partner_success(data)
