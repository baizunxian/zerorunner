from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.projectquery import ProjectQuery, ProjectIn, ProjectId
from autotest.services.api.project import ProjectService

router = APIRouter()


@router.post('/list', description="项目列表")
async def project_list(params: ProjectQuery):
    data = await ProjectService.list(params)
    return partner_success(data)


@router.post('/getAllProject', description="获取所有项目")
async def get_all_project():
    data = await ProjectService.get_all()
    return partner_success(data)


@router.post('/saveOrUpdate', description="更新保存项目")
async def save_or_update(params: ProjectIn):
    data = await ProjectService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description="删除")
async def deleted(params: ProjectId):
    data = await ProjectService.deleted(params)
    return partner_success(data)


@router.post('/getProjectTree', description="获取项目树结构")
async def get_project_tree():
    """
    项目树结构
    :return:
    """
    data = await ProjectService.get_project_tree()
    return partner_success(data)
