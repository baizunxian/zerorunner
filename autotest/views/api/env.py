from flask import Blueprint, request

from autotest.services.api_services.env import EnvService
from autotest.utils.api import partner_success

bp = Blueprint('env', __name__, url_prefix='/api/env')


@bp.route('/list', methods=['POST'])
def env_list():
    """
    获取列表
    :return:
    """
    data = EnvService.list(**request.json)
    return partner_success(data=data)


@bp.route('/getEnvById', methods=['POST'])
def get_env_by_id():
    """
    获取列表
    :return:
    """
    env_id = request.json.get("id", None)
    data = EnvService.get_env_by_id(env_id)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update_env():
    """
    更新保存环境信息
    :return:
    """
    data = EnvService.save_or_update(**request.json)
    return partner_success(data=data.id)


@bp.route('/deleted', methods=['POST'])
def delete_env():
    """
    删除环境
    :return:
    """
    parsed_data = request.json
    env_id = parsed_data.get('id', None)
    EnvService.deleted(env_id)
    return partner_success()
