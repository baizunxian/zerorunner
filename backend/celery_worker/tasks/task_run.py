# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from autotest.schemas.api.timed_task import TaskKwargsIn
from celery_worker.worker import celery
from .test_case import async_run_testcase
from .ui_case import async_run_ui


@celery.task(name="zerorunner.batch_async_run_testcase")
def batch_async_run_testcase(**kwargs: typing.Any):
    """批量执行"""
    params = TaskKwargsIn(**kwargs)
    if params.case_ids:
        kwargs['run_type'] = "case"
        for api_id in params.case_ids:
            async_run_testcase.apply_async(args=[api_id], kwargs=kwargs, __business_id=api_id)
    if params.ui_ids:
        kwargs['run_type'] = "ui"
        for ui_id in params.ui_ids:
            async_run_ui.apply_async(args=[ui_id], kwargs=kwargs, __business_id=ui_id)
