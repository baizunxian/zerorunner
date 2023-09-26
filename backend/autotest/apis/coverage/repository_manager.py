from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.coverage.repository_manager import RepositoryListQuery
from autotest.services.coverage.repository_manager import RepositoryManagerService

router = APIRouter()


@router.post('/getRepositoryList', description="获取仓库列表")
async def get_repository_list(params: RepositoryListQuery):
    data = await RepositoryManagerService.get_projects(params)
    return partner_success(data)


@router.post('/getBranches', description="获取仓库分支")
async def get_repository_list(params: RepositoryListQuery):
    data = await RepositoryManagerService.get_branches(params)
    return partner_success(data)
