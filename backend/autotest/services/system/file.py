import base64
import os
import typing
import uuid
from io import StringIO

from fastapi import UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from loguru import logger
from config import config
from autotest.models.system_models import FileInfo
from autotest.schemas.system.file import FileIn, FileId
import aiofiles
from pathlib import Path
from autotest.utils.common import get_str_uuid


class FileService:
    """文件"""

    @staticmethod
    async def upload(file: UploadFile) -> typing.Dict[str, str]:
        """文件上传"""
        if not file:
            raise FileNotFoundError('请选择上传文件！')
        file_dir = config.TEST_FILES_DIR
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        extend_file = file.filename.split(".")
        extend_name = extend_file[-1] if len(extend_file) > 1 else None

        file_name = f'{str(uuid.uuid4()).replace("-", "").upper()}'
        if extend_name:
            file_name = f"{file_name}.{extend_name}"
        abs_file_path = Path(file_dir).joinpath(file_name).as_posix()
        contents = await file.read()
        file_size = len(contents) / 1024
        async with aiofiles.open(abs_file_path, "wb") as f:
            await f.write(contents)
        file_params = FileIn(id=get_str_uuid(),
                             name=file_name,
                             file_path=abs_file_path,
                             extend_name=extend_name,
                             original_name=file.filename,
                             file_size=file_size,
                             content_type=file.content_type)

        file_info = await FileInfo.create(file_params.dict())
        logger.info(f'文件保存--> {abs_file_path}')
        file_id = file_info.id
        data = {
            'id': file_id,
            'url': f'/file/download/{file_id}',
            'name': file.filename,
            'original_name': file.filename,
        }
        return data

    @staticmethod
    async def save_base64_file(base64_content: str, filename: str) -> typing.Dict[str, str]:
        """文件上传"""
        if not base64_content:
            raise FileNotFoundError('请选择上传文件！')
        file_dir = config.TEST_FILES_DIR
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        extend_file = filename.split(".")
        extend_name = extend_file[-1] if len(extend_file) > 1 else None

        file_name = f'{str(uuid.uuid4()).replace("-", "").upper()}'
        if extend_name:
            file_name = f"{file_name}.{extend_name}"
        abs_file_path = Path(file_dir).joinpath(file_name).as_posix()
        contents = base64.b64decode(base64_content)
        file_size = len(contents) / 1024
        async with aiofiles.open(abs_file_path, "wb") as f:
            await f.write(contents)
        file_params = FileIn(id=get_str_uuid(),
                             name=file_name,
                             file_path=abs_file_path,
                             extend_name=extend_name,
                             original_name=filename,
                             file_size=file_size,
                             content_type=extend_name)

        file_info = await FileInfo.create(file_params.dict())
        logger.info(f'文件保存--> {abs_file_path}')
        file_id = file_info.id
        data = {
            'id': file_id,
            'url': f'/file/download/{file_id}',
            'name': file_name,
            'original_name': filename,
        }
        return data

    @staticmethod
    async def download(file_id: str) -> typing.Union[FileResponse, HTMLResponse]:
        file_info = await FileInfo.get(file_id)
        if not file_info:
            logger.error(f'{file_id} 文件不存在！')
            return HTMLResponse(content="文件不存在")
        file_dir = Path(config.TEST_FILES_DIR).joinpath(file_info.name).as_posix()
        if not os.path.isfile(file_dir):
            logger.error(f'{file_info.name}文件不存在！')
            return HTMLResponse(content="文件不存在")

        return FileResponse(path=file_dir, filename=file_info.original_name)

    @staticmethod
    async def deleted(file_id: str) -> int:
        """删除文件"""
        return await FileInfo.delete(file_id)

    @staticmethod
    async def get_file_by_id(params: FileId):
        file_info = await FileInfo.get(params.id)
        if not file_info:
            logger.error('文件不存在！')
            raise FileNotFoundError('文件不存在！')
        file_dir = os.path.join(config.TEST_FILES_DIR, file_info.file_name)
        if not os.path.isfile(file_dir):
            logger.error('文件不存在！')
            raise FileNotFoundError('文件不存在！')

        data = {
            'id': file_info.id,
            'url': f'/file/download/{file_info.file_name}',
            'name': file_info.original_name,
            'static_url': f'/static/files/{file_info.file_name}'
        }
        return data
