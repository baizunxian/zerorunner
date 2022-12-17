import traceback
from typing import Any, Dict, Text
from loguru import logger
from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.serialize.api_serializes.project import ProjectQuerySchema
from autotest.models.api_models import ProjectInfo, Functions, ModuleInfo
from autotest.services.api_services.functions import FunctionsService
from autotest.utils.api import parse_pagination, jsonable_encoder
from autotest.utils.common import get_user_id_by_token


class ProjectService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取项目列表
        :param kwargs:
        :return:
        """
        query_data = ProjectQuerySchema(**kwargs).dict()
        data = parse_pagination(
            ProjectInfo.get_project_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': _result
        }
        result.update(**pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "ProjectInfo":
        """
        更新保存项目
        :param kwargs:
        :return:
        """
        user_id = get_user_id_by_token()
        project_name = kwargs.get('name')
        project_info = ProjectInfo.get(kwargs.get('id')) if kwargs.get('id', None) else ProjectInfo()
        if project_info.id:
            if config.EDIT_SWITCH:
                if project_info.created_by != user_id:
                    raise ValueError(partner_errmsg.get(codes.CANNOT_EDIT_CREATED_BY_YOURSELF).format('项目'))
            if project_info.name != project_name:
                if ProjectInfo.get_project_by_name(project_name):
                    raise ValueError(partner_errmsg.get(codes.PROJECT_NAME_EXIST))
        else:
            if ProjectInfo.get_project_by_name(project_name):
                raise ValueError(partner_errmsg.get(codes.PROJECT_NAME_EXIST))
        try:
            debug_info = Functions.get_by_project_id(project_info.id)
            FunctionsService.save_or_update(
                **dict(id=debug_info.id if debug_info else None, project_id=project_info.id))
        except Exception as err:
            logger.error(traceback.format_exc())

        project_info.update(**kwargs)
        return project_info

    @staticmethod
    def deleted(id: int):
        """
        删除项目
        :param id:
        :return:
        """
        project = ProjectInfo.get(id)
        user_id = get_user_id_by_token()
        if project:
            module = ModuleInfo.get_module_by_project_id(id)
            if config.EDIT_SWITCH:
                if project.created_by != user_id:
                    raise ValueError(partner_errmsg.get(codes.CANNOT_DELETE_CREATED_BY_YOURSELF).format('项目'))
            if module:
                raise ValueError(partner_errmsg.get(codes.PROJECT_HAS_MODULE_ASSOCIATION))
            project.delete()
            try:
                debug_info = Functions.get_by_project_id(project.id)
                debug_info.delete()
            except Exception as err:
                logger.error(traceback.format_exc())

    @staticmethod
    def get_project_tree(project_id: int = None):
        project_list = ProjectInfo.get_project_list(id=project_id).all()
        module_list = ModuleInfo.get_list().all()

        project_tree_list = []

        for project in project_list:
            project_dict = jsonable_encoder(project)
            project_dict["children"] = []
            project_dict["disabled"] = True
            for module in module_list:
                if module.project_id == project.id:
                    project_dict["children"].append(jsonable_encoder(module))
                    project_dict["disabled"] = False
            project_tree_list.append(project_dict)
        return project_tree_list
