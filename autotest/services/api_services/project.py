import traceback
from typing import Any, Dict, Text

from loguru import logger

from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.serialize.api_serializes.project import ProjectListSchema, ProjectQuerySchema
from autotest.models.api_models import ProjectInfo, DebugTalk, ModuleInfo
from autotest.services.api_services.debug_talk import DebugTalkService
from autotest.utils.api import parse_pagination
from autotest.utils.common import get_user_id_by_token


class ProjectService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取项目列表
        :param kwargs:
        :return:
        """
        query_data = ProjectQuerySchema().load(kwargs)
        data = parse_pagination(
            ProjectInfo.get_project_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': ProjectListSchema().dump(_result, many=True)
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
            debug_info = DebugTalk.get_by_project_id(project_info.id)
            DebugTalkService.save_or_update(
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
                debug_info = DebugTalk.get_by_project_id(project.id)
                debug_info.delete()
            except Exception as err:
                logger.error(traceback.format_exc())
