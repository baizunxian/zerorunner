import os
import traceback
import uuid
from typing import Dict, Text

from flask import request, make_response, send_from_directory
from loguru import logger

from autotest.config import config


class FileService:
    """文件"""

    @staticmethod
    def upload() -> Dict[Text, Text]:
        """文件上传"""
        file = request.files.get('file')
        if not file:
            raise FileNotFoundError('请选择上传文件！')
        file_dir = config.TEST_FILES_DIR
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_name = f'{uuid.uuid4().hex[:6]}{file.filename}'
        abs_file_path = os.path.join(file_dir, file_name)
        file.save(abs_file_path)
        logger.info(f'文件保存--> {abs_file_path}')
        data = {
            'abspath': abs_file_path,
            'url': f'/file/download/{file_name}',
            'name': file_name
        }
        return data

    @staticmethod
    def download(file_path: Text) -> "make_response":
        file_dir = os.path.join(config.TEST_FILES_DIR, file_path)
        if not os.path.isfile(file_dir):
            logger.error('文件不存在！')
            raise FileNotFoundError('文件不存在！')

        response = make_response(
            send_from_directory(config.TEST_FILES_DIR, file_path, file_path, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment;" "filename*=UTF-8''{utf_filename}".format(
            utf_filename=file_path.split('/')[-1].encode('utf8'))
        return response

    @staticmethod
    def deleted(name: Text):
        """删除文件"""
        file_dir = os.path.join(config.TEST_FILES_DIR, name)
        try:
            if os.path.exists(file_dir):
                os.remove(file_dir)
        except Exception as err:
            logger.error(traceback.format_exc())
