# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.models.ui_models import UiElement
from autotest.schemas.ui.ui_element import UiElementIn, UiElementQuery


class UiElementServer:
    """页面元素服务"""

    @staticmethod
    async def list(params: UiElementQuery):
        return await UiElement.get_list(params)

    @staticmethod
    async def save_or_update(params: UiElementIn):
        return await UiElement.save_or_update(params)

    @staticmethod
    async def deleted(id: int):
        return await UiElement.deleted(id)
