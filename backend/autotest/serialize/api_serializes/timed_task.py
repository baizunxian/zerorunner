from typing import Dict, Optional, Text, List, Union
from pydantic import root_validator, BaseModel
from autotest.exc import codes
from autotest.exc.exceptions import ParameterError
from autotest.exc.partner_message import partner_errmsg
from autotest.models.api_models import Crontab, TimedTask
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class TimedTasksQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[int, Text]]]
    name: Optional[Text]
    created_by_name: Optional[Text]


class TimedTasksListSchema(BaseListSchema):
    name: Optional[Text]
    task: Optional[Text]
    args: Optional[Text]
    kwargs: Optional[Text]
    queue: Optional[Text]
    exchange: Optional[Text]
    routing_key: Optional[Text]
    enabled: Optional[int]
    total_run_count: Optional[int]
    description: Optional[Text]
    crontab_id: Optional[int]
    crontab_str: Optional[Text]
    interval_id: Optional[int]
    run_type: Optional[Text]
    project_id: Optional[int]
    project_name: Optional[Text]
    module_id: Optional[int]
    module_name: Optional[Text]
    suite_id: Optional[int]
    case_ids: Optional[Text]
    expires: Optional[Text]
    last_run_at: Optional[Text]
    date_changed: Optional[Text]

    @root_validator
    def root_validator(cls, data) -> Dict:
        if data.get("crontab_id", None):
            crontab = Crontab.get(data["crontab_id"])
            data["crontab_str"] = ' '.join(
                [crontab.minute, crontab.hour, crontab.day_of_month, crontab.month_of_year, crontab.day_of_week])
        if 'case_ids' in data and isinstance(data['case_ids'], str):
            data['case_ids'] = list(map(int, data['case_ids'].split(',')))
        return data


class CrontabSaveSchema(BaseModel):
    """Crontab"""

    crontab_str: Optional[Text]

    @root_validator
    def root_validator(cls, data) -> Dict:
        if not data.get('crontab_str', None):
            raise ParameterError('crontab 不能为空!')
        crontab_time = data.get('crontab_str', '').split(' ')
        if len(crontab_time) != 5:
            raise ParameterError('定时配置参数格式不正确!')
        data['crontab_time'] = crontab_time
        return data


class TimedTasksSaveOrUpdateSchema(BaseModel):
    """定时任务保存更新"""
    id: Optional[int]
    case_ids: Optional[List[int]]
    module_id: Optional[int]
    project_id: Optional[int]
    run_type: Optional[Text]
    crontab_str: Optional[Text]
    module_ids: Optional[Text]
    name: Optional[Text]
    task: Optional[Text]
    description: Optional[Text]

    @root_validator
    def root_validator(cls, data):
        t_id = data.get('id', None)
        name = data.get('name', None)
        task_info = TimedTask.get(t_id) if t_id else None
        if task_info:
            if name != task_info.name:
                if TimedTask.get_task_by_name(name):
                    raise ParameterError(partner_errmsg.get(codes.TASK_NAME_EXIST))
        else:
            if TimedTask.get_task_by_name(name):
                raise ParameterError(partner_errmsg.get(codes.TASK_NAME_EXIST))
        if not data.get("name", None):
            raise ParameterError("请填写定时任务名称!")
        if not data.get('task', None):
            data['task'] = 'autotest.tasks.test_case.run_timed_task'
        if data.get('case_ids', None) and isinstance(data['case_ids'], str):
            data['case_ids'] = list(map(str, data['case_ids']))
        return data
