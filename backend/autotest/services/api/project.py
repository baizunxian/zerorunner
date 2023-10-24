import typing

from autotest.utils.response.codes import CodeEnum
from autotest.exceptions.exceptions import ParameterError
from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.schemas.api.projectquery import ProjectQuery, ProjectIn, ProjectId


class ProjectService:
    @staticmethod
    async def list(params: ProjectQuery) -> typing.Dict:
        """
        获取项目列表
        :param params:
        :return:
        """
        data = await ProjectInfo.get_list(params)
        return data

    @staticmethod
    async def get_all() -> typing.Dict:
        """
        获取项目列表
        :return:
        """
        data = await ProjectInfo.get_all()
        return data

    @staticmethod
    async def save_or_update(params: ProjectIn) -> typing.Dict:
        """
        更新保存项目
        :param params:
        :return:
        """
        if params.id:
            project_info = await ProjectInfo.get(params.id)
            if project_info.name != params.name:
                if await ProjectInfo.get_project_by_name(params.name):
                    raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        else:
            if await ProjectInfo.get_project_by_name(params.name):
                raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)

        return await ProjectInfo.create_or_update(params.dict())

    @staticmethod
    async def deleted(params: ProjectId) -> int:
        """
        删除项目
        :param params:
        :return:
        """
        relation_module = await ModuleInfo.get_module_by_project_id(params.id)
        if relation_module:
            raise ParameterError(CodeEnum.PROJECT_HAS_MODULE_ASSOCIATION)
        return await ProjectInfo.delete(params.id)

    @staticmethod
    async def get_project_tree() -> typing.List:
        project_list = await ProjectInfo.get_all()
        module_list = await ModuleInfo.get_all()

        project_tree_list = []

        for project in project_list:
            project["children"] = []
            project["disabled"] = True
            if module_list:
                for module in module_list:
                    if module["project_id"] == project["id"]:
                        project["children"].append(module)
                        project["disabled"] = False
            project_tree_list.append(project)
        return project_tree_list
