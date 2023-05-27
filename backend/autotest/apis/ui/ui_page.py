# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.corelibs.http_response import partner_success
from autotest.schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId
from autotest.services.ui.ui_page import UiPageServer

router = APIRouter()


@router.post("/list")
async def ui_page_list(params: UiPageQuery):
    data = await UiPageServer.list(params)
    return partner_success(data)


@router.post("/getPageById")
async def get_page_by_id(params: UiPageId):
    data = await UiPageServer.get_page_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate")
async def save_or_update(params: UiPageIn):
    data = await UiPageServer.save_or_update(params)
    return partner_success(data)


@router.post("/deleted")
async def deleted(params: UiPageId):
    data = await UiPageServer.deleted(params.id)
    return partner_success(data)
