from typing import Dict

from marshmallow import Schema, fields, post_dump, EXCLUDE, post_load

from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.models.api_models import Crontab, TimedTask
from autotest.serialize.base_serialize import BaseListSchema


class TimedTasksQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    name = fields.Str()
    created_by_name = fields.Str()


class TimedTasksListSchema(BaseListSchema):
    id = fields.Int()
    name = fields.Str()
    task = fields.Str()
    args = fields.Str()
    kwargs = fields.Str()
    queue = fields.Str()
    exchange = fields.Str()
    routing_key = fields.Str()
    enabled = fields.Int()
    total_run_count = fields.Int()
    description = fields.Str()
    crontab_id = fields.Int()
    crontab_str = fields.Str()
    interval_id = fields.Int()
    run_type = fields.Str()
    project_id = fields.Int()
    project_name = fields.Str()
    module_id = fields.Int()
    module_name = fields.Str()
    suite_id = fields.Int()
    case_ids = fields.Str()
    expires = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))
    last_run_at = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))
    date_changed = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))

    @post_dump
    def post_dump(self, data, **kwargs) -> Dict:
        if data.get("crontab_id", None):
            crontab = Crontab.get(data["crontab_id"])
            data["crontab_str"] = ' '.join(
                [crontab.minute, crontab.hour, crontab.day_of_month, crontab.month_of_year, crontab.day_of_week])
        if 'case_ids' in data:
            data['case_ids'] = list(map(int, data['case_ids'].split(',')))
        return data


class CrontabSaveSchema(Schema):
    """Crontab"""

    class Meta:
        unknown = EXCLUDE

    crontab_str = fields.Str()

    @post_load
    def post_load(self, data, **kwargs) -> Dict:
        if not data.get('crontab_str', None):
            raise ValueError('crontab 不能为空!')
        crontab_time = data.get('crontab_str', '').split(' ')
        if len(crontab_time) != 5:
            raise ValueError('定时配置参数格式不正确!')
        data['crontab_time'] = crontab_time
        return data


class TimedTasksSaveOrUpdateSchema(Schema):
    """定时任务保存更新"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    case_ids = fields.List(fields.Int())
    module_id = fields.Int(allow_none=True)
    project_id = fields.Int()
    run_type = fields.Str()
    crontab_str = fields.Str()
    module_ids = fields.Str()
    name = fields.Str()
    task = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        t_id = data.get('id', None)
        name = data.get('name', None)
        task_info = TimedTask.get(t_id) if t_id else None
        if task_info:
            if name != task_info.name:
                if TimedTask.get_task_by_name(name):
                    raise ValueError(partner_errmsg.get(codes.TASK_NAME_EXIST))
        else:
            if TimedTask.get_task_by_name(name):
                raise ValueError(partner_errmsg.get(codes.TASK_NAME_EXIST))
        if not data.get("name", None):
            raise ValueError("请填写定时任务名称!")
        if not data.get('task', None):
            data['task'] = 'autotest.tasks.test_case.run_timed_task'
        if data.get('case_ids', None):
            data['case_ids'] = list(map(str, data['case_ids']))
        return data
