from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.job.task_record import TaskRecordQuery
from autotest.services.job.task_record import TaskRecordServer

router = APIRouter()


@router.post('/taskList', description="异步任务列表")
async def project_list(params: TaskRecordQuery):
    data = await TaskRecordServer.list(params)
    return partner_success(data)
