from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.timed_task import TimedTasksQuerySchema, TimedTasksInSchema, TimedTasksId, CrontabSaveSchema
from autotest.services.api.timed_task import TimedTasksService, CrontabService

router = APIRouter()


@router.post('/list', description="定时任务列表")
async def timed_tasks_list(params: TimedTasksQuerySchema):
    data = await TimedTasksService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="新增，修改定时任务")
async def save_or_update(params: TimedTasksInSchema):
    data = await TimedTasksService.save_or_update(params)
    return partner_success(data)


@router.post('/taskSwitch', description="定时任务开关")
async def task_switch(params: TimedTasksId):
    data = await TimedTasksService.task_switch(params)
    return partner_success(data)


@router.post('/deleted', description="删除任务定时任务")
async def deleted_tasks(params: TimedTasksId):
    data = await TimedTasksService.deleted(params)
    return partner_success(data)


@router.post('/checkCrontab', description="校验crontab")
async def check_crontab(params: CrontabSaveSchema):
    data = await CrontabService.check_crontab(params.crontab)
    return partner_success(data)


@router.post('/runOnceJob', description="运行一次任务")
async def run_once_job(params: TimedTasksId):
    data = await TimedTasksService.run_once_job(params)
    return partner_success(data)
