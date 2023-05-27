# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.models.ui_models import UiPage
from autotest.schemas.ui.ui_page import UiPageQuery, UiPageIn


class UiPageServer:
    """页面服务"""

    @staticmethod
    async def list(params: UiPageQuery):
        return await UiPage.get_list(params)

    @staticmethod
    async def save_or_update(params: UiPageIn):
        return await UiPage.create_or_update(params.dict())

    @staticmethod
    async def deleted(id: int):
        return await UiPage.deleted(id)
