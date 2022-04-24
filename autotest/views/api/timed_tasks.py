import datetime
import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.models.api_models import TimedTask, PeriodicTaskChanged
from autotest.services.api_services.timed_task import TimedTasksService
from autotest.utils.api import partner_success, json_required, login_verification

bp = Blueprint('timed_tasks', __name__, url_prefix='/api/timedTasks')


@bp.route('/list', methods=['POST'])
@login_verification
@json_required
def timed_tasks_list():
    """定时任务列表"""
    try:
        result = TimedTasksService.list(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=result)


@bp.route('/saveOrUpdate', methods=['POST'])
@login_verification
@json_required
def save_or_update():
    """新增，修改定时任务"""
    try:
        result = TimedTasksService.save_or_update(**request.json)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=result)


@bp.route('/TaskSwitch', methods=['POST'])
@login_verification
@json_required
def task_switch():
    """定时任务开关"""
    parsed_data = request.json
    task_id = parsed_data.get('t_id', None)  # t id
    task_info = TimedTask.get(task_id)
    task_switch_state = task_info.enabled
    if task_switch_state == 1:
        task_info.enabled = 0
    else:
        task_info.enabled = 1
    task_info.save()

    task_changed = PeriodicTaskChanged.get(1)
    task_changed.last_update = datetime.datetime.now()
    task_changed.save()
    task_info.case_ids = task_info.case_ids.split(',') if task_info.case_ids else None
    task_info.iaa_push_ids = task_info.iaa_push_ids.split(',') if task_info.iaa_push_ids else None
    task = TimedTasksSchema().dump(task_info)
    return partner_success(task)


@bp.route('/deleted', methods=['POST'])
@login_verification
@json_required
def deleted_tasks():
    """删除任务"""
    try:
        parsed_data = request.json
        task_id = parsed_data.get('id', None)
        TimedTasksService.deleted(task_id)
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success()
