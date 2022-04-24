from flask import request, g
from loguru import logger

from autotest.corelibs.backend import celery
from autotest.services.api_services.test_case import CaseService


@celery.task()
def async_run_case(**kwargs):
    CaseService.run(**kwargs)
