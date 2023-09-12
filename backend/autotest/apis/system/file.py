from fastapi import APIRouter, UploadFile, File

from autotest.utils.response.http_response import partner_success
from autotest.schemas.system.file import FileId
from autotest.services.system.file import FileService

router = APIRouter()


@router.post('/upload', description="文件上传")
async def upload(file: UploadFile = File(...)):
    result = await FileService.upload(file)
    return partner_success(result)


@router.get('/download/{file_id}', description="文件下载")
async def download(file_id: str):
    result = await FileService.download(file_id)
    return result


@router.get('/getFileById', description="根据id获取文件下载地址")
async def get_file_by_id(params: FileId):
    return await FileService.get_file_by_id(params)


@router.post('/deleted', description="文件删除")
async def deleted(params: FileId):
    data = await FileService.get_file_by_id(params)
    return partner_success(data)
