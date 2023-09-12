from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.system.menu import MenuIn, MenuDel, MenuViews
from autotest.services.system.menu import MenuService

router = APIRouter()


@router.post('/allMenu', description="获取所有菜单数据")
async def all_menu():
    data = await MenuService.all_menu()
    return partner_success(data)


@router.post('/getAllMenus', description="获取菜单嵌套结构")
async def get_all_menus():
    data = await MenuService.all_menu_nesting()
    return partner_success(data)


@router.post('/saveOrUpdate', description="新增或者更新menu")
async def save_or_update(params: MenuIn):
    # return partner_success(code=codes.PARTNER_CODE_FAIL, msg="演示环境不保存！")
    await MenuService.save_or_update(params)
    return partner_success()


@router.post('/deleted', description="删除菜单")
async def delete_menu(params: MenuDel):
    data = await MenuService.deleted(params)
    return partner_success(data)


@router.post('/setMenuViews', description="设置菜单访问量")
async def set_menu_views(params: MenuViews):
    await MenuService.set_menu_views(params)
    return partner_success()
