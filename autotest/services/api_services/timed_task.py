import datetime
import json
import traceback
from typing import Dict, Any, Union, Text

from loguru import logger

from autotest.models.api_models import TimedTask, Crontab, \
    PeriodicTaskChanged
from autotest.serialize.api_serializes.timed_task import (
    TimedTasksQuerySchema,
    TimedTasksListSchema,
    TimedTasksSaveOrUpdateSchema,
    CrontabSaveSchema)
from autotest.utils.api import parse_pagination
from autotest.utils.common import get_user_info_by_token


class CrontabService:
    @staticmethod
    def save_or_update(**kwargs: Any) -> "Crontab":
        try:
            parsed_data = CrontabSaveSchema().load(kwargs)
            crontab_time = parsed_data.get('crontab_time')
            minute = crontab_time[0],  # 分
            hour = crontab_time[1],  # 小时
            day_of_month = crontab_time[2],  # 日期
            day_of_week = crontab_time[3],  # 周
            month_of_year = crontab_time[-1],  # 月份
        except Exception as err:
            raise ValueError(err)
        crontab_query_params = {
            'minute': minute,
            'hour': hour,
            'day_of_week': day_of_week,
            'day_of_month': day_of_month,
            'month_of_year': month_of_year
        }
        crontab = Crontab.get_crontab_by_parameter(**crontab_query_params)
        if not crontab:
            try:
                crontab = Crontab()
                crontab.minute = minute
                crontab.hour = hour
                crontab.day_of_month = day_of_month
                crontab.month_of_year = month_of_year
                crontab.day_of_week = day_of_week
                crontab.save()
            except Exception as err:
                logger.error(err)
                raise ValueError(err)
        return crontab


class TimedTasksService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        定时任务列表
        """
        query_data = TimedTasksQuerySchema().load(kwargs)
        data = parse_pagination(TimedTask.get_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': TimedTasksListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "TimedTask":
        """
        保存或更新定时任务
        """
        parsed_data = TimedTasksSaveOrUpdateSchema().load(kwargs)
        task_id = parsed_data.get('id')
        name = parsed_data.get('name')
        project_id = parsed_data.get('project_id')
        case_ids = parsed_data.get('case_ids')
        run_type = parsed_data.get('run_type')
        timed_task = TimedTask.get(task_id) if task_id else TimedTask()

        try:
            crontab = CrontabService.save_or_update(**kwargs)
            user_info = get_user_info_by_token()

            task_kwargs = {
                'ids': case_ids,
                'name': name,
                'project_id': project_id,
                'run_type': run_type,
                'run_mode': 3,
                'base_url': '',
                'ex_user_id': user_info.get('id'),
                'ex_user_name': user_info.get('nickname')
            }
            parsed_data['case_ids'] = ','.join(case_ids)
            parsed_data['crontab_id'] = crontab.id
            parsed_data['kwargs'] = json.dumps(task_kwargs)
            timed_task.update(**parsed_data)

            PeriodicTaskChangedService.update()
            return timed_task
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def deleted(task_id: Union[str, int]):
        """
        删除定时任务
        """
        task_info = TimedTask.get(task_id)
        if task_info:
            task_info.delete(True)
            PeriodicTaskChangedService.update()

    @staticmethod
    def task_switch(task_id: Union[str, int]):
        """
        定时任务开关
        """
        task_info = TimedTask.get(task_id)
        task_info.enabled = 0 if task_info.enabled == 1 else 1
        task_info.save()
        task_changed = PeriodicTaskChanged.get_data()
        task_changed.last_update = datetime.datetime.now()
        task_changed.save()
        task = TimedTasksListSchema().dump(task_info)
        return task


class PeriodicTaskChangedService:
    @staticmethod
    def update() -> "PeriodicTaskChanged":
        try:
            periodic_task_changed = PeriodicTaskChanged.get_data()
            periodic_task_changed.last_update = datetime.datetime.now()
            periodic_task_changed.save()
            return periodic_task_changed
        except Exception as err:
            logger.error(traceback.format_exc())
            raise ValueError(err)
