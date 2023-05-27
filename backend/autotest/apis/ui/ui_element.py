# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.corelibs.http_response import partner_success
from autotest.schemas.ui.ui_element import UiElementQuery, UiElementIn
from autotest.services.ui.ui_element import UiElementServer

router = APIRouter()


@router.post("/list")
async def ui_page_list(params: UiElementQuery):
    data = await UiElementServer.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate")
async def save_or_update(params: UiElementIn):
    data = await UiElementServer.save_or_update(params)
    return partner_success(data)


@router.post("/deleted")
async def save_or_update(params: UiElementIn):
    data = await UiElementServer.save_or_update(params)
    return partner_success(data)
