# -*- coding: utf-8 -*-
# @author: xiaobai
# import asyncio
import asyncio
import uuid
from abc import ABC
from celery import Celery, Task
from celery._state import _task_stack
from celery.signals import after_setup_logger
from celery.worker.request import Request
from loguru import logger
from autotest.config import config
from autotest.corelibs.local import g
from autotest.corelibs.logger import InterceptHandler
from autotest.db.redis import init_redis_pool
from autotest.utils.async_converter import AsyncIOPool


class TaskRequest(Request):
    """重写task request 设置 trace_id 这里可以设置所有透传过来的参数"""

    def __init__(self, *args, **kwargs):
        super(TaskRequest, self).__init__(*args, **kwargs)
        self.set_trace_id()

    def set_trace_id(self):
        """这里为了设置消息发送是的trace_id能与请求保持一致特殊处理"""
        trace_id = self.request_dict.get("trace_id", str(uuid.uuid4()))
        g.trace_id = trace_id


# @celeryd_after_setup.connect
# def setup_direct_queue(sender, instance, **kwargs):
#     """此信号在工作实例设置之后但在它调用运行之前发送。这意味着该 选项中的任何队列都已启用，日志记录已设置等"""
#     queue_name = '{0}.dq'.format(sender)  # sender is the nodename of the worker
#
#
# @after_task_publish.connect
# def pre_task_received(body, **kwargs):
#     """任务发布后触发"""
#     queue_name = '{0}.dq'.format(body)
#
#
# @task_received.connect
# def task_received_in(request: Request, **kwargs):
#     """收到任务时触发"""
#     queue_name = '{0}.dq'.format(request)


# @before_task_publish.connect
# def receiver_before_task_publish(headers=None, **kwargs):
#     """
#     任务发送前触发
#     :param headers: 任务上下文
#     :param kwargs:
#     :return:
#     """


# @task_prerun.connect
# def receiver_task_pre_run(task: Task, *args, **kwargs):
#     """
#     任务执行前执行
#     :param task_id: 任务id
#     :param task: task 实例
#     :param args:
#     :param kwargs:
#     :return:
#     """


# @after_setup_logger.connect
# def setup_loggers(logger, *args, **kwargs):
#     """logger 初始化统一处理日志格式"""
#     logger.handlers = []
#     logger.addHandler(InterceptHandler())


def create_celery():
    """
    celery 初始类
    :return:
    """

    class ContextTask(Task, ABC):
        Request = TaskRequest

        def delay(self, *args, **kwargs):
            return self.apply_async(args, kwargs)

        def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                        link=None, link_error=None, shadow=None, **options):
            headers = {"headers": {"trace_id": g.trace_id}}
            if options:
                options.update(headers)
            else:
                options = headers
            return super(ContextTask, self).apply_async(args, kwargs, task_id, producer, link, link_error,
                                                        shadow, **options)

        def on_success(self, retval, task_id, args, kwargs):
            """任务成功时回调"""
            logger.info("on_success")
            return super(ContextTask, self).on_success(retval, task_id, args, kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """任务失败时回调"""
            logger.info("on_failure")
            return super(ContextTask, self).on_failure(exc, task_id, args, kwargs, einfo)

        def __call__(self, *args, **kwargs):
            """重写call方法 支持异步函数的运行"""
            g.trace_id = self.request.trace_id
            _task_stack.push(self)
            self.push_request(args=args, kwargs=kwargs)
            g.redis = AsyncIOPool.run_in_pool(init_redis_pool())
            try:
                if asyncio.iscoroutinefunction(self.run):
                    return AsyncIOPool.run_in_pool(self.run(*args, **kwargs))
                else:
                    return self.run(*args, **kwargs)
            finally:
                self.pop_request()
                _task_stack.pop()

    _celery_: Celery = Celery("zerorunner-celery-worker", task_cls=ContextTask)
    _celery_.config_from_object(config)

    return _celery_


celery = create_celery()

# celery_worker 专用于celery的worker
# worker windows 启动，只能单线程
# celery -A celery_worker.worker.celery worker --pool=solo -l INFO
# worker linux  启动
# celery -A celery_worker.worker.celery worker --pool=solo -c 10 -l INFO  linux 启动
# beat
# celery -A celery_worker.worker.celery beat  -l INFO  启动节拍器，定时任务需要
# beat 数据库
# celery -A celery_worker.worker.celery beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO

if __name__ == '__main__':
    import sys

    celery.start(argv=sys.argv[1:])
