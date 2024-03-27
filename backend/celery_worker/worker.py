# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio
import datetime
import json
import logging
import traceback
import uuid
from abc import ABC

from celery import Celery, Task
from celery._state import _task_stack
from celery.signals import setup_logging, task_prerun
from celery.worker.request import Request

from autotest.init.logger_init import InterceptHandler, logger
from autotest.schemas.job.task_record import TaskRecordIn
from autotest.services.job.task_record import TaskRecordServer
from autotest.utils.async_converter import AsyncIOPool
from autotest.utils.local import g
from autotest.utils.serialize import MyJsonDecode
from config import config

WorkerPool = AsyncIOPool()


# @celeryd_after_setup.connect
# def setup_direct_queue(sender, instance, **kwargs):
#     """此信号在工作实例设置之后但在它调用运行之前发送。这意味着该选项中的任何队列都已启用，日志记录已设置等"""
#     queue_name = '{0}.dq'.format(sender)  # sender is the nodename of the worker
#
#
# @after_task_publish.connect
# def pre_task_received(body, **kwargs):
#     """任务发布后触发"""
#     time.sleep(30)
#     queue_name = '{0}.dq'.format(body)
#     logger.info(f'sleep 30 s {queue_name}')


#
#
# @task_received.connect
# def task_received_in(request: Request, **kwargs):
#     """收到任务时触发"""
#     queue_name = '{0}.dq'.format(request)
#     time.sleep(30)
#     logger.info(f'sleep 30 s {queue_name}')


# @before_task_publish.connect
# def receiver_before_task_publish(headers=None, **kwargs):
#     """
#     任务发送前触发
#     :param headers: 任务上下文
#     :param kwargs:
#     :return:
#     """


@task_prerun.connect
def receiver_task_pre_run(task: Task, *args, **kwargs):
    """
    任务执行前执行
    :param task: task 实例
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # 获取定时任务id，如果是定时任务则记录定时任务id
        business_id = task.request.properties.get("__business_id", None)
        task_type = task.request.properties.get("__task_type", None)
        params = TaskRecordIn(
            task_name=task.name,
            task_type=task_type,
            task_id=task.request.id,
            start_time=datetime.datetime.now(),
            status="RUNNING",
            business_id=business_id,
            args=json.dumps(task.request.args, cls=MyJsonDecode),
            kwargs=json.dumps(task.request.kwargs, cls=MyJsonDecode),
        )
        WorkerPool.run(TaskRecordServer.save_or_update(params))
        logger.info(f"异步任务提交--> task id [{task.request.id}]")
    except:
        logger.error(f"t异步任务提交--> 错误 error:\n{traceback.format_exc()}")


@setup_logging.connect
def setup_loggers(*args, **kwargs):
    """logger 初始化统一处理日志格式"""
    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOGGER_LEVEL)


class TaskRequest(Request):
    """重写task request 设置 trace_id 这里可以设置所有透传过来的参数"""

    def __init__(self, *args, **kwargs):
        super(TaskRequest, self).__init__(*args, **kwargs)
        self.set_trace_id()

    def set_trace_id(self):
        """这里为了设置消息发送是的trace_id能与请求保持一致特殊处理"""
        trace_id = self.request_dict.get("trace_id", str(uuid.uuid4()))
        g.trace_id = trace_id


def create_celery():
    """
    job 初始类
    :return:
    """

    class NewCelery(Celery):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def send_task(self, *args, **kwargs):
            headers = {"headers": {"trace_id": g.trace_id}}
            if kwargs:
                kwargs.update(headers)
            else:
                kwargs = headers
            return super().send_task(*args, **kwargs)

    class ContextTask(Task, ABC):
        Request = TaskRequest

        def delay(self, *args, **kwargs):
            return self.apply_async(args, kwargs)

        def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                        link=None, link_error=None, shadow=None, **options):
            __task_type = options.get("__task_type", None)
            __task_type = __task_type if __task_type else 10
            headers = {"headers": {"trace_id": g.trace_id}, "__task_type": __task_type}
            if options:
                options.update(headers)
            else:
                options = headers
            return super(ContextTask, self).apply_async(args, kwargs, task_id, producer, link, link_error,
                                                        shadow, **options)

        def on_success(self, retval, task_id, args, kwargs):
            """任务成功时回调"""
            logger.info("on_success")
            self.handel_task_record("SUCCESS", str(retval))
            return super(ContextTask, self).on_success(retval, task_id, args, kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """任务失败时回调"""
            logger.info("on_failure")
            self.handel_task_record("FAILURE", str(exc), einfo.traceback)
            return super(ContextTask, self).on_failure(exc, task_id, args, kwargs, einfo)

        def handel_task_record(self, status: str, result: str, err: str = None):
            """
            处理任务记录
            :param status: 状态
            :param result: 结果
            :param err: 异常信息
            :return:
            """
            try:
                record_task_info = WorkerPool.run(TaskRecordServer.get_task_record_by_id(self.request.id))
                if record_task_info:
                    record_task_info["status"] = status
                    record_task_info["result"] = result
                    record_task_info["traceback"] = err
                    record_task_info["end_time"] = datetime.datetime.now()
                    params = TaskRecordIn(**record_task_info)
                    WorkerPool.run(TaskRecordServer.save_or_update(params))
            except:
                logger.error(f"异步任务执行结果保存错误！ task id [{self.request.id}]:\n{traceback.format_exc()}")

        def __call__(self, *args, **kwargs):
            """重写call方法 支持异步函数的运行"""
            g.trace_id = self.request.trace_id
            _task_stack.push(self)
            self.push_request(args=args, kwargs=kwargs)
            try:
                if asyncio.iscoroutinefunction(self.run):
                    return WorkerPool.run(self.run(*args, **kwargs))
                else:
                    return self.run(*args, **kwargs)
            finally:
                self.pop_request()
                _task_stack.pop()

    _celery_: Celery = NewCelery("zerorunner-job-worker", task_cls=ContextTask)
    _celery_.config_from_object(config)
    # 自动发现各个app下的tasks.py文件
    _celery_.autodiscover_tasks()

    return _celery_


celery = create_celery()

# celery_worker 专用于celery的worker
# worker windows 启动，只能单线程
# celery -A celery_worker.worker worker --pool=solo -l INFO
# worker linux  启动
# celery -A celery_worker.worker worker --pool=solo -c 10 -l INFO  linux 启动
# beat
# celery -A celery_worker.worker beat  -l INFO  启动节拍器，定时任务需要
# beat 数据库
# celery -A celery_worker.worker beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO

if __name__ == '__main__':
    import sys

    celery.start(argv=sys.argv[1:])
