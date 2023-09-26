from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.functions import FuncQuery, FuncListQuery, FuncIn, FuncDebug, FuncId
from autotest.services.api.functions import FunctionsService

router = APIRouter()


@router.post('/list', description="获取自定义函数列表")
async def get_debug_talk_list(params: FuncQuery):
    data = await FunctionsService.list(params)
    return partner_success(data)


@router.post('/getFuncInfo', description="获取自定义函数详情")
async def get_debug_talk_info(params: FuncQuery):
    data = await FunctionsService.get_function_info(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="更新保存")
async def save_debug_talk(params: FuncIn):
    """
    更新保存
    :return:
    """
    # return partner_success(code=codes.PARTNER_CODE_FAIL, msg='演示环境不保存！')
    data = await FunctionsService.save_or_update(params)
    return partner_success(data)


@router.post('/getFuncList', description="获取函数列表")
async def get_func_list(params: FuncListQuery):
    try:
        data = await FunctionsService.get_function_by_id(params)
        func_list = data.get('func_list')
        return partner_success(func_list)
    except Exception as err:
        raise ValueError(f"查询函数名称失败:{err}")


@router.post('/debugFunc', description="脚本调试")
async def debug_func(params: FuncDebug):
    result = await FunctionsService.debug_func(params)
    return partner_success({'result': result})


@router.post('/deleted', description="删除脚本")
async def debug_func(params: FuncId):
    data = await FunctionsService.deleted(params)
    return partner_success(data)
