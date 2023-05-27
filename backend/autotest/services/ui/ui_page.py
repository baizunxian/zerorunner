# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.exceptions.exceptions import ParameterError
from autotest.models.ui_models import UiPage
from autotest.schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId


class UiPageServer:
    """页面服务"""

    @staticmethod
    async def list(params: UiPageQuery):
        return await UiPage.get_list(params)

    @staticmethod
    async def get_page_by_id(params: UiPageId):
        if not params.id:
            raise ParameterError("id不能为空")
        page_info = await UiPage.get_page_by_id(params.id)
        if not page_info:
            raise ParameterError("UI页面信息不存在")
        return page_info

    @staticmethod
    async def save_or_update(params: UiPageIn):
        page_info = await UiPage.create_or_update(params.dict())
        return await UiPageServer.get_page_by_id(UiPageId(id=page_info['id']))

    @staticmethod
    async def deleted(id: int):
        return await UiPage.deleted(id)
