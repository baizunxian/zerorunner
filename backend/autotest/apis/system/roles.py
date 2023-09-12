from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.system.roles import RoleQuery, RoleIn, RoleDel
from autotest.services.system.role import RolesService

router = APIRouter()


@router.post('/list', description="获取角色列表")
async def all_roles(params: RoleQuery):
    data = await RolesService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="新增或更新角色")
async def save_or_update(params: RoleIn):
    data = await RolesService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description="删除角色")
async def deleted(params: RoleDel):
    data = await RolesService.deleted(params)
    return partner_success(data)
