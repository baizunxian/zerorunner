import json
import traceback
import typing

from celery.schedules import crontab as celery_crontab
from loguru import logger

from autotest.exceptions.exceptions import ParameterError
from autotest.models.celery_beat_models import TimedTask, Crontab, IntervalSchedule, PeriodicTaskChanged, TimedTaskCase
from autotest.schemas.api.timed_task import TimedTasksQuerySchema, CrontabSaveSchema, TimedTasksInSchema, TimedTasksId, \
    TaskKwargsIn, IntervalIn, TimedTaskCaseQuery
from autotest.utils.current_user import current_user
from autotest.utils.response.codes import CodeEnum
from celery_worker.worker import celery


class CrontabService:
    @staticmethod
    async def save_or_update(params: CrontabSaveSchema) -> typing.Dict[str, typing.Any]:
        if not params.crontab:
            raise ParameterError("crontab表达式不能为空!")

        if not await CrontabService.check_crontab(params.crontab):
            raise ParameterError("请输入正确的crontab表达式!")

        cron = celery_crontab(*params.crontab.split(" "))
        crontab_query_params = {
            'minute': cron._orig_minute,
            'hour': cron._orig_hour,
            'day_of_week': cron._orig_day_of_week,
            'day_of_month': cron._orig_day_of_month,
            'month_of_year': cron._orig_month_of_year
        }
        crontab = await Crontab.get_crontab_by_parameter(**crontab_query_params)
        if not crontab:
            try:
                crontab = await Crontab.create_or_update(crontab_query_params)
                return crontab
            except Exception as err:
                logger.error(err)
                raise ValueError(err)
        return crontab

    @staticmethod
    async def check_crontab(crontab: str):
        try:
            celery_crontab(*crontab.split(' '))
        except Exception as err:
            # raise ValueError("crontab格式错误！")
            return False
        return True


class IntervalService:
    @staticmethod
    async def save_or_update(params: IntervalIn) -> typing.Dict:

        interval = await IntervalSchedule.get_interval_by_parameter(**params.dict())
        if not interval:
            try:
                interval = await IntervalSchedule.create_or_update(params.dict())
                return interval
            except Exception as err:
                logger.error(err)
                raise ValueError(err)
        return interval


class TaskChangedService:
    @staticmethod
    async def update_changed():
        await PeriodicTaskChanged.update_changed()


class TimedTasksService:
    @staticmethod
    async def list(params: TimedTasksQuerySchema) -> typing.Dict:
        """
        定时任务列表
        """
        result = await TimedTask.get_list(params)
        for data in result["rows"]:
            if "case_ids" in data:
                case_ids = data.get("case_ids", None)
                data["case_ids"] = list(map(int, case_ids.split(','))) if case_ids else []
            if "task_tags" in data:
                task_tags = data.get("task_tags", None)
                data["task_tags"] = task_tags.split(',') if task_tags else []

        return result

    @staticmethod
    async def get_task_case_info(params: TimedTaskCaseQuery):
        if params.type == "case":
            data = await TimedTaskCase.get_by_case(params)
        elif params.type == 'ui':
            data = []
        elif params.type == "script":
            data = []
        else:
            raise ValueError("type参数错误！")
        return data

    @staticmethod
    async def save_or_update(params: TimedTasksInSchema) -> typing.Dict:
        """
        保存或更新定时任务
        """

        exist_tasks = await TimedTask.get_task_by_name(params.name)
        if params.id:
            task_info = await TimedTask.get(params.id)
            if not task_info:
                raise ParameterError("定时任务不存在！")
            if params.name != task_info.name:
                if exist_tasks:
                    raise ParameterError(CodeEnum.TASK_NAME_EXIST)
        else:
            if exist_tasks:
                raise ParameterError(CodeEnum.TASK_NAME_EXIST)
        if not params.task:
            params.task = 'zerorunner.batch_async_run_testcase'
        if params.case_ids:
            params.case_ids = list(map(str, params.case_ids))
        user_info = await current_user()

        try:

            if params.task_type == "crontab":
                crontab = await CrontabService.save_or_update(CrontabSaveSchema(crontab=params.crontab))
                params.crontab_id = crontab.get("id")
            elif params.task_type == "interval":
                interval = await IntervalService.save_or_update(
                    IntervalIn(every=params.interval_every, period=params.interval_period))
                params.interval_id = interval.get("id")
            else:
                raise ParameterError("请选择调度类型！")

            task_kwargs = TaskKwargsIn(
                name=params.name,
                case_ids=params.case_ids,
                case_env_id=params.case_env_id,
                ui_ids=params.ui_ids,
                ui_env_id=params.ui_env_id,
                project_id=params.project_id,
                run_type="case",
                run_mode=30,
                exec_user_id=user_info.get("id"),
                exec_user_name=user_info.get("nickname"),
            )
            case_ids = params.case_ids
            ui_ids = params.ui_ids
            task_case_params = []
            params.case_ids = ','.join(params.case_ids)
            params.task_tags = ','.join(params.task_tags)
            params.kwargs = task_kwargs.json()
            timed_task = await TimedTask.create_or_update(params.dict())
            task_id = timed_task.get("id")
            await TaskChangedService.update_changed()
            if case_ids:
                task_case_params.extend([dict(task_id=task_id,
                                              case_id=case_id,
                                              type="case") for case_id in case_ids])

            if ui_ids:
                task_case_params.extend([dict(task_id=task_id,
                                              case_id=case_id,
                                              type="ui") for case_id in
                                         ui_ids])
            if task_case_params:
                await TimedTaskCase.deleted_by_task_id(task_id)
                await TimedTaskCase.batch_create(task_case_params)

            return timed_task
        except Exception as err:
            logger.error(f"保存定时任务错误：\n{traceback.format_exc()}")
            raise ValueError(f"保存定时任务错误: \n{err}")

    @staticmethod
    async def deleted(params: TimedTasksId) -> int:
        """
        删除定时任务
        """
        timed_task = await TimedTask.get(params.id)
        if timed_task and timed_task.enabled:
            raise ParameterError("定时任务运行中，请先停止后再删除！")
        rowcount = await TimedTask.delete(params.id)
        return rowcount

    @staticmethod
    async def task_switch(params: TimedTasksId) -> typing.Dict:
        """
        定时任务开关
        """
        task_info = await TimedTask.get(params.id, to_dict=True)
        if not task_info:
            return {}
        enabled = task_info.get("enabled", None)
        task_info_data = {
            "id": task_info["id"],
            "enabled": not enabled,
            # "start_time": datetime.datetime.now(),
            # "expires": datetime.datetime.now() + datetime.timedelta(minutes=5)
        }
        if not enabled:
            # 停止任务时重置最后运行时间
            task_info_data["last_run_at"] = None

        task_info = await TimedTask.create_or_update(task_info_data)
        await PeriodicTaskChanged.update_changed()
        return task_info

    @staticmethod
    async def get_count_by_user():
        """获取用户api数量"""
        user_info = await current_user()
        count_info = await TimedTask.get_count_by_user_id(user_info.get("id", None))
        if not count_info:
            return 0
        if count_info:
            return count_info.get("count", 0)

    @staticmethod
    async def run_once_job(params: TimedTasksId):
        task_info = await TimedTask.get(params.id)
        if task_info:
            kwargs = json.loads(task_info.kwargs) if task_info.kwargs else None
            args = json.loads(task_info.args) if task_info.args else None
            celery.send_task(name=task_info.task,
                             args=args,
                             kwargs=kwargs,
                             queue=task_info.queue,
                             __task_type=20,
                             __business_id=task_info.id)
