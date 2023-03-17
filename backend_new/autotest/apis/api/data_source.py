# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:47
from fastapi import APIRouter

from autotest.corelibs.http import partner_success
from autotest.schemas.api.data_source import SourceQuery, SourceIn, SourceId
from autotest.services.api.data_source import DataSourceService, SourceInfo, ExecuteParam

router = APIRouter()


@router.post('/sourceList', description="获取数据源列表")
async def get_source_list(params: SourceQuery):
    data = await DataSourceService.get_source_list(params)
    return partner_success(data)


@router.post('/saveOrUpdateSource', description="保存")
async def save_or_update_source(params: SourceIn):
    data = await DataSourceService.save_or_update(params)
    return partner_success(data)


@router.post('/deletedSource', description="删除")
async def deleted_source(params: SourceId):
    data = await DataSourceService.deleted_source(params)
    return partner_success(data)


@router.post('/testConnect', description="测试连接")
async def test_connect(params: SourceInfo):
    """
    测试连接
    :return:
    """
    data = await DataSourceService.test_connect(params)
    return partner_success(data)


@router.post('/dbList', description="数据列表")
def get_db_list():
    source_id = request.get_json().get('source_id', None)
    data = DataSourceService.get_db_list(source_id)
    return partner_success(data)


@router.post('/tableList', description="表列表")
def get_table_list():
    """
    表列表
    :return:
    """
    source_id = request.get_json().get('source_id', None)
    databases = request.get_json().get('databases', None)
    data = DataSourceService.get_table_list(source_id, databases)
    return partner_success(data)


@router.post('/columnList', description="获取表字段")
def get_column_list():
    source_id = request.get_json().get('source_id', None)
    databases = request.get_json().get('databases', None)
    data = DataSourceService.get_column_list(source_id, databases)
    return partner_success(data)


@router.post('/mysql/execute', description="mysql 查询")
def mysql_execute(params: ExecuteParam):
    data = DataSourceService.execute(params)
    return partner_success(data)
