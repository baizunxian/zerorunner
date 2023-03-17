# -*- coding: utf-8 -*-
# @author: xiaobai
from celery import group

from autotest.celery_worker import celery
from autotest.celery_worker.base import run_async
from autotest.schemas.api.projectquery import ProjectIn
from autotest.services.api.project import ProjectService


@celery.task
def add(i):
    return 1 + i


@celery.task
def save_project(params):
    data = ProjectIn(**params)
    run_async(ProjectService.save_or_update(data))
