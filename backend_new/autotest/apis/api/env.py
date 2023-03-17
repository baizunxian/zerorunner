from fastapi import APIRouter

from autotest.corelibs.http import partner_success
from autotest.schemas.api.env import EnvQuery, EnvId, EnvIn, BindingDataSourceIn
from autotest.services.api.env import EnvService, EnvDataSourceService

router = APIRouter()


@router.post('/list', description="环境列表")
async def env_list(params: EnvQuery):
    data = await EnvService.list(params)
    return partner_success(data)


@router.post('/getEnvById', description="获取列表")
async def get_env_by_id(params: EnvQuery):
    data = await EnvService.get_env_by_id(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="更新保存环境信息")
async def save_or_update_env(params: EnvIn):
    data = await EnvService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description="删除环境")
async def delete_env(params: EnvId):
    data = await EnvService.deleted(params)
    return partner_success(data)


@router.post('/getDataSourceByEnvId', description="根据env_id获取数据源")
async def get_data_source_by_env_id(params: EnvId):
    data = await EnvDataSourceService.get_by_env_id(params)
    return partner_success(data)


@router.post('/bindingDataSource', description="绑定关联数据源")
async def binding_data_source(params: BindingDataSourceIn):
    data = await EnvDataSourceService.binding_data_source(params)
    return partner_success(data)


@router.post('/unbindingDataSource', description="解绑关联数据源")
async def unbinding_data_source(params: BindingDataSourceIn):
    data = await EnvDataSourceService.unbinding_data_source(params)
    return partner_success(data)
