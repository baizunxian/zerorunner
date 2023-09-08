from autotest.models.coverage_models import RepositoryManager
from autotest.schemas.coverage.repository_manager import RepositoryListQuery
from autotest.utils.handle_git import HandleGit


class RepositoryManagerService:

    @staticmethod
    async def get_projects(params: RepositoryListQuery):
        return await HandleGit.get_projects()
    @staticmethod
    async def get_branches(params: RepositoryListQuery):
        return await HandleGit.get_branches()

    @staticmethod
    async def list(params: RepositoryListQuery):
        return await RepositoryManager.get_list(params)
