from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.module import ModuleQuery, ModuleIn, ModuleId
from autotest.services.api.module import ModuleService

router = APIRouter()


@router.post('/list', description="模块列表")
async def module_list(params: ModuleQuery):
    data = await ModuleService.list(params)
    return partner_success(data)


@router.post('/getAllModule', description="获取所有模块")
async def get_all_module():
    data = await ModuleService.get_all()
    return partner_success(data)


@router.post('/saveOrUpdate', description="更新保存项目")
async def save_or_update(params: ModuleIn):
    data = await ModuleService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description="删除模块")
async def deleted(params: ModuleId):
    data = await ModuleService.deleted(params)
    return partner_success(data)
