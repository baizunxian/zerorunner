import sys

from celery.local import PromiseProxy
from celery import Celery as CeleryClass, Task
from flask import request


class _CeleryState:
    """
    记住（celery，app）元组的配置。从SQLAlchemy建模
    """

    def __init__(self, celery, app):
        self.celery = celery
        self.app = app


class Celery(CeleryClass):

    def __init__(self, app=None):
        super(Celery, self).__init__()
        # 若app为None, 则在 init_app 才初始化
        self.app = app

        class ContextTask(Task):
            abstract = True
            flask_app = None

            def __call__(self, *_args, **_kwargs):
                # 如果celery没有init_app
                # 则celery.tasks()注册的任务将会因为flask_app为None而调用失败
                with self.flask_app.app_context():
                    self.user_id = request
                    return Task.__call__(self, *_args, **_kwargs)

        self.Task = ContextTask

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        if 'celery' in app.extensions:
            raise ValueError('Already registered extension CELERY.')
        self.Task.flask_app = app
        app.extensions['celery'] = _CeleryState(self, app)
        # celery 里面管理配置非常复杂. 留了不少接口改配置,但是这些接口的配置会互相覆盖!!
        # 因此不要在不同的接口改配置, 整个项目只在这里改配置!!

        self.conf.update(app.config)


celery = Celery()


def gen_celery_for_worker():
    """
        hack !!
        由于celery作为worker跑的时候,并不会创建flask app
        因此我们需要单独处理worker跑的情况
    """
    from autotest.app import create_app
    create_app()
    global celery
    return celery


# celery_worker 专用于celery的worker
# celery -A autotest.corelibs.backend.celery_worker worker --pool=solo -l INFO  windows 启动，只能单线程
# celery -A autotest.corelibs.backend.celery_worker beat  -l INFO  启动节拍器，定时任务需要
# celery -A autotest.corelibs.backend.celery_worker beat -S scheduler.schedulers:DatabaseScheduler -l INFO
# celery -A autotest.corelibs.backend.celery_worker beat -S autotest.corelibs.scheduler.schedulers:DatabaseScheduler -l INFO
# 当不是作为worker跑的时候,就不需要初始化celery_worker
# PromiseProxy 用于lazy load, 如果不操作celery_worker, 就不会有初始化的开销

# celery worker -A autotest.corelibs.backend.celery_worker --loglevel=INFO --pool=solo
celery_worker = PromiseProxy(gen_celery_for_worker)
