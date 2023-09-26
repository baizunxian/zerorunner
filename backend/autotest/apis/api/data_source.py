# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:47
from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.data_source import SourceQuery, SourceIn, SourceId
from autotest.services.api.data_source import DataSourceService, SourceInfo, ExecuteParam, SourceIdIn, SourceTableIn, \
    CreateTableIn

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
async def get_source_list(params: SourceIdIn):
    data = await DataSourceService.get_db_list(params)
    return partner_success(data)


@router.post('/tableList', description="表列表")
async def get_table_list(params: SourceTableIn):
    """
    表列表
    :return:
    """
    data = await DataSourceService.get_table_list(params)
    return partner_success(data)


@router.post('/columnList', description="获取表字段")
async def get_column_list(params: SourceTableIn):
    data = await DataSourceService.get_column_list(params.source_id, params.databases)
    return partner_success(data)


@router.post('/mysql/execute', description="mysql 查询")
async def mysql_execute(params: ExecuteParam):
    data = await DataSourceService.execute(params)
    return partner_success(data)


@router.post('/showCreateTable', description="查询建表语句")
async def show_create_table(params: CreateTableIn):
    data = await DataSourceService.show_create_table(params)
    return partner_success(data)
