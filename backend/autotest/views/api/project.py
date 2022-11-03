from flask import Blueprint, request

from autotest.config import config
from autotest.services.api_services.project import ProjectService
from autotest.utils.api import partner_success

bp = Blueprint('project', __name__, url_prefix='/api/project')
auth = config.Authentication


@bp.route('/list', methods=['POST'])
def project_list():
    """
    项目列表
    :return:
    """
    data = ProjectService.list(**request.json)
    return partner_success(data=data)


@bp.route('/saveOrUpdate', methods=['POST'])
def save_or_update():
    """
    更新保存项目
    :return:
    """
    data = ProjectService.save_or_update(**request.json)
    return partner_success(data.id)


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    删除
    :return:
    """
    parsed_data = request.json
    id = parsed_data.get('id', None)
    ProjectService.deleted(id)
    return partner_success()
