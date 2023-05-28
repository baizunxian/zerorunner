# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.models.ui_models import UiElement
from autotest.schemas.ui.ui_element import UiElementIn, UiElementQuery


class UiElementServer:
    """页面元素服务"""

    @staticmethod
    async def list(params: UiElementQuery):
        """获取元素列表"""
        return await UiElement.get_list(params)

    @staticmethod
    async def save_or_update(params: UiElementIn):
        """保存或更新元素信息"""
        return await UiElement.create_or_update(params.dict())

    @staticmethod
    async def deleted(id: int):
        """删除元素信息"""
        return await UiElement.delete(id)

    @staticmethod
    async def get_page_element_tree():
        """获取页面元素树"""
        element_all = await UiElement.get_element_all()
        if not element_all:
            return []
        data = []
        for element in element_all:
            ...
        return await UiElement.get_element_all()
