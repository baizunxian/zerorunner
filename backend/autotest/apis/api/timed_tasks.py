from fastapi import APIRouter

from autotest.db.session import provide_async_session_router
from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.timed_task import TimedTasksQuerySchema, TimedTasksInSchema, TimedTasksId, CrontabSaveSchema, \
    TimedTaskCaseQuery
from autotest.services.api.timed_task import TimedTasksService, CrontabService

router = APIRouter()


@router.post('/list', description="定时任务列表")
async def timed_tasks_list(params: TimedTasksQuerySchema):
    data = await TimedTasksService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="新增，修改定时任务")
@provide_async_session_router
async def save_or_update(params: TimedTasksInSchema):
    data = await TimedTasksService.save_or_update(params)
    return partner_success(data)


@router.post('/taskSwitch', description="定时任务开关")
async def task_switch(params: TimedTasksId):
    raise RuntimeError("验收环境关闭该功能，可以手都执行查看效果😊")
    data = await TimedTasksService.task_switch(params)
    return partner_success(data)


@router.post('/deleted', description="删除任务定时任务")
async def deleted_tasks(params: TimedTasksId):
    data = await TimedTasksService.deleted(params)
    return partner_success(data)


@router.post('/checkCrontab', description="定时任务校验crontab")
async def check_crontab(params: CrontabSaveSchema):
    data = await CrontabService.check_crontab(params.crontab)
    return partner_success(data)


@router.post('/runOnceJob', description="定时任务运行一次任务")
async def run_once_job(params: TimedTasksId):
    data = await TimedTasksService.run_once_job(params)
    return partner_success(data)


@router.post('/getTaskCaseInfo', description="获取定时任务关联case")
async def get_task_case_info(params: TimedTaskCaseQuery):
    data = await TimedTasksService.get_task_case_info(params)
    return partner_success(data)
