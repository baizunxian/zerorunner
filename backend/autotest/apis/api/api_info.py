import json

from fastapi import APIRouter
from loguru import logger

from autotest.corelibs.http_response import partner_success
from autotest.schemas.api.api_info import ApiQuery, ApiId, ApiInfoIn, ApiRunSchema
from autotest.services.api.api_info import ApiInfoService
from celery_worker.tasks.test_case import async_run_api

router = APIRouter()


@router.post('/list', description="获取接口列表")
async def api_list(params: ApiQuery):
    result = await ApiInfoService.list(params)
    return partner_success(result)


@router.post('/getApiInfo', description="获接口信息详情")
async def get_case_info(params: ApiId):
    """
    获取用例信息
    :return:
    """
    case_info = await ApiInfoService.detail(params)
    return partner_success(case_info)


@router.post('/saveOrUpdate', description="更新保存接口")
async def save_or_update(params: ApiInfoIn):
    case_info = await ApiInfoService.save_or_update(params)
    return partner_success(case_info)


@router.post('/setCaseStatus', description="接口失效生效")
def set_case_status():
    parsed_data = request.json
    ApiInfoService.set_api_status(**parsed_data)
    return partner_success()


@router.post('/deleted', description="删除接口")
def deleted():
    """
    删除用例
    :return:
    """
    parsed_data = request.json
    c_id = parsed_data.get('id', None)
    ApiInfoService.deleted(c_id)
    return partner_success()


@router.post('/run', description="运行接口")
async def run_test(params: ApiRunSchema):
    """
    运行用例
    :return:
    """

    if params.run_type == 20:
        logger.info('异步执行用例 ~')
        async_run_api.delay(**params.dict())
        return partner_success(code=0, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
    else:
        summary = await ApiInfoService.run(params)  # 初始化校验，避免生成用例是出错
        return partner_success(summary)


@router.post('/debugApi', description="debug接口")
async def debug_api(params: ApiInfoIn):
    data = await ApiInfoService.debug_api(params)
    return partner_success(data)


@router.post('/testRunCase', description="测试运行用例")
def test_run_case():
    """
    测试运行用例
    :return:
    """
    data = run_timed_task(**request.json)
    return partner_success(data)


@router.post('/postman2case', description="文件转用例")
def postman2case():
    """
    postman 文件转用例
    :return:
    """
    postman_file = request.files.get('file', None)
    if not postman_file:
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择导入的postman，json文件！')
    if postman_file.filename.split('.')[-1] != 'json':
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg='请选择json文件导入！')
    json_body = json.load(postman_file)
    data = ApiInfoService.postman2api(json_body, **request.form)
    return partner_success(data)
