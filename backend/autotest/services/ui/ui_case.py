# -*- coding: utf-8 -*-
# @author: xiaobai
from autotest.exceptions.exceptions import ParameterError
from autotest.models.ui_models import UiCase
from autotest.schemas.ui.ui_case import UiCaseQuery, UiCaseId, UiCaseIn


class UiCaseServer:
    """ui用例服务"""

    @staticmethod
    async def list(params: UiCaseQuery):
        """获取用例列表"""
        return await UiCase.get_list(params)

    @staticmethod
    async def get_case_by_id(params: UiCaseId):
        """根据id获取用例信息"""
        if not params.id:
            raise ParameterError("id不能为空")
        page_info = await UiCase.get_page_by_id(params.id)
        if not page_info:
            raise ParameterError("UI页面信息不存在")
        return page_info

    @staticmethod
    async def save_or_update(params: UiCaseIn):
        """保存或更新用例信息"""
        page_info = await UiCase.create_or_update(params.dict())
        return await UiCaseServer.get_case_by_id(UiCaseId(id=page_info['id']))

    @staticmethod
    async def deleted(id: int):
        """删除用例信息"""
        return await UiCase.delete(id)
