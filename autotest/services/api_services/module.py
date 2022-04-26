from typing import Dict, Union, Any, Text

from autotest.config import config
from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.serialize.api_serializes.module import ModuleListSchema, ModuleQuerySchema
from autotest.models.api_models import ModuleInfo, CaseInfo
from autotest.utils.api import parse_pagination
from autotest.utils.common import get_user_id_by_token


class ModuleService:
    """模块处理类"""

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取模块列表
        :param kwargs: 查询参数
        :return:
        """
        parsed_data = ModuleQuerySchema().load(kwargs)
        data = parse_pagination(ModuleInfo.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': ModuleListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "ModuleInfo":
        """
        模块保存方法
        :param kwargs:
        :return:
        """
        user_id = get_user_id_by_token()
        module_info = ModuleInfo.get(kwargs.get('id')) if kwargs.get('id', None) else ModuleInfo()
        modules = ModuleInfo.get_module_by_name(kwargs.get('name'))
        # 当模块关联的包发生变更时，原始包移除模块信息
        if module_info.id:
            if config.EDIT_SWITCH:
                if module_info.created_by != user_id:
                    raise ValueError(partner_errmsg.get(codes.CANNOT_EDIT_CREATED_BY_YOURSELF).format('模块'))
            if module_info.name != kwargs.get('name'):
                if modules:
                    raise ValueError(partner_errmsg.get(codes.MODULE_NAME_EXIST))
        else:
            if modules:
                raise ValueError(partner_errmsg.get(codes.MODULE_NAME_EXIST))
        module_info.update(**kwargs)
        return module_info

    @staticmethod
    def deleted(id: Union[str, int]):
        """
        删除模块
        :param id:
        :return:
        """
        user_id = get_user_id_by_token()
        module = ModuleInfo.get(id)
        if module:
            case_info = CaseInfo.get_case_by_module_id(id).count()
            if config.EDIT_SWITCH:
                if module.created_by != user_id:
                    raise ValueError(partner_errmsg.get(codes.CANNOT_DELETE_CREATED_BY_YOURSELF).format('模块'))
            if case_info:
                raise ValueError(partner_errmsg.get(codes.MODULE_HAS_CASE_ASSOCIATION))
            module.delete()
