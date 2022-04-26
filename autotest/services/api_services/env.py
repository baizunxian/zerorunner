import traceback
from typing import Dict, Any

from loguru import logger

from autotest.serialize.api_serializes.env import EnvQuerySchema, EnvListSchema, EnvSaveOrUpdateSchema
from autotest.models.api_models import Env
from autotest.utils.api import parse_pagination


class EnvService:
    @staticmethod
    def list(**kwargs: Any) -> Dict:
        parsed_data = EnvQuerySchema().load(kwargs)
        data = parse_pagination(Env.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': EnvListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> Env:
        parsed_data = EnvSaveOrUpdateSchema().load(kwargs)
        env_id = kwargs.get('id', None)
        env_info = Env.get(env_id) if env_id else Env()
        env_info.update(**parsed_data)
        return env_info

    @staticmethod
    def deleted(id: int):
        """删除项目"""
        try:
            env = Env.get(id)
            env.delete()
        except Exception as err:
            logger.error(traceback.format_exc())
