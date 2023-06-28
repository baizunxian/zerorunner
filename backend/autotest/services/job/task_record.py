# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from autotest.models.celery_beat_models import CeleryTaskRecord
from autotest.schemas.job.task_record import TaskRecordQuery, TaskRecordIn


class TaskRecordServer:

    @staticmethod
    async def list(params: TaskRecordQuery) -> typing.Any:
        """
        获取任务记录列表
        :param params:
        :return:
        """
        return await CeleryTaskRecord.get_list(params)

    @staticmethod
    async def save_or_update(params: TaskRecordIn) -> typing.Dict:
        """
        保存或更新任务记录
        :param params:
        :return:
        """
        task_info = await TaskRecordServer.get_task_record_by_id(params.task_id)
        params = params.dict(exclude_none=True)
        if task_info:
            task_info.update(params)
            params = task_info
        return await CeleryTaskRecord.create_or_update(params)

    @staticmethod
    async def get_task_record_by_id(task_id: str) -> typing.Dict:
        """
        通过任务ID获取任务记录
        :param task_id:
        :return:
        """
        return await CeleryTaskRecord.get_task_record_by_task_id(task_id)
