from flask import Blueprint, request

from autotest.services.sys_services.file import FileService
from autotest.utils.api import partner_success

bp = Blueprint('file', __name__, url_prefix='/api/file')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    文件上传
    :return:
    """
    result = FileService.upload()
    return partner_success(result)


@bp.route('/download/<path:file_path>', methods=['GET'])
def download(file_path):
    """
    文件下载
    :return:
    """
    result = FileService.download(file_path)
    return result


@bp.route('/deleted', methods=['POST'])
def deleted():
    """
    文件删除
    :return:
    """
    parsed_data = request.json
    name = parsed_data.get('name', None)
    FileService.deleted(name)
    return partner_success()
