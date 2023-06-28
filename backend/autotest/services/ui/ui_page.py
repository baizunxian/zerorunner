# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.exceptions.exceptions import ParameterError
from autotest.models.ui_models import UiPage, UiElement
from autotest.schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId


class UiPageServer:
    """页面服务"""

    @staticmethod
    async def list(params: UiPageQuery):
        """获取页面列表"""
        return await UiPage.get_list(params)

    @staticmethod
    async def get_page_by_id(params: UiPageId):
        """根据id获取页面信息"""
        if not params.id:
            raise ParameterError("id不能为空")
        page_info = await UiPage.get_page_by_id(params.id)
        if not page_info:
            raise ParameterError("UI页面信息不存在")
        return page_info

    @staticmethod
    async def save_or_update(params: UiPageIn):
        """保存或更新页面信息"""
        page_info = await UiPage.create_or_update(params.dict())
        return await UiPageServer.get_page_by_id(UiPageId(id=page_info['id']))

    @staticmethod
    async def deleted(id: int):
        """删除页面信息"""
        return await UiPage.delete(id)

    @staticmethod
    async def get_all_page_element():
        """获取页面元素信息"""
        all_element = await UiElement.get_all()
        all_page = await UiPage.get_all()
        page_element = []
        for page in all_page:
            page['elements'] = []
            page['disabled'] = True
            for element in all_element:
                if element['page_id'] == page['id']:
                    page['elements'].append(element)
                    page['disabled'] = False
            page_element.append(page)
        return page_element
