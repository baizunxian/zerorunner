import os

db_user = 'root'
db_password = 'root'
db_host = '127.0.0.1'
db_port = 3306

CONFIGS = {
    'DEBUG': True,
    # mysql数据库的配置信息
    'SQLALCHEMY_DATABASE_URI': f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/zero_autotest?charset=UTF8MB4',
    # 动态追踪修改设置，如未设置只会提示警告
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # 查询时会显示原始SQL语句
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_POOL_SIZE': 20,
    'SQLALCHEMY_MAX_OVERFLOW': 500,
    'SQLALCHEMY_POOL_TIMEOUT': 10,
    'SQLALCHEMY_POOL_RECYCLE': 7200,
    # 设置密钥，可以通过 base64.b64encode(os.urandom(48)) 来生成一个指定长度的随机字符串
    'SECRET_KEY': "ghhBljAa0uzw2afLqJOXrukORE4BlkTY/1vaMuDh6opQ3uwGYtsDUyxcH62Aw3ju",
    'BASEDIR': os.path.abspath(os.path.dirname(__file__)),
    'TEST_DIR': os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'suite'),
    'TEST_FILES_DIR': os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'files'),
    'REPORT_DIR': os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'reports'),

    # redis 信息
    'REDIS_URL': 'redis://:@127.0.0.1:6379/4',
    'REDIS_MAX_CONNECTIONS': 1024,

    # Celery 配置
    'CELERY_FORCE_ROOT': True,
    'timezone': "Asia/Shanghai",
    'enable_utc': False,
    'result_backend': 'redis://:@127.0.0.1:6379/8',
    'broker_url': 'redis://:@127.0.0.1:6379/8',
    'accept_content': ['json'],
    'result_serializer': 'json',

    # 非常重要,有些情况下可以防止死锁
    'CELERYD_FORCE_EXECV': True,
    # 并发worker数
    'worker_concurrency': 10,
    'worker_prefetch_multiplier': 1,
    # 每个worker最多执行100万个任务就会被销毁，可防止内存泄露
    'worker_max_tasks_per_child': 100,
    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
    'task_time_limit': 60,
    # 列队配置
    'task_routes': {
        # 'blog.tasks.sms.send_sms': {'queue': 'record'},
        # 'blog.tasks.log.asynclog': {'queue': 'celery'},
        # 'blog.tasks.dbcrud.login_device_operate': {'queue': 'record'},
        # 'blog.tasks.lock_user.locked_user': {'queue': 'record'},
    },
    # borker池，默认是10
    'broker_pool_limit': 12,
    'redis_max_connections': 20,
    'broker_transport_options': {
        'visibility_timeout': 3600,
        'max_connections': 400
    },
    'result_backend_transport_options': {'visibility_timeout': 3600},
    # 任务过期时间 只是记录登录日志 并非重要事务 因此过期时间设置为2分钟
    'result_expires': 120,
    # backend缓存结果的数目，默认5000
    'result_cache_max': 1000,
    # 导入任务模块
    'imports': (
        'autotest.tasks',
    ),

    # 定时任务
    'beat_dburi': f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/zero_autotest?charset=UTF8MB4',
    # 定时任务
    # 'CELERYBEAT_SCHEDULE': {
    # 'batch_main_hrun': {
    #     'task': 'autotest.tasks.case.batch_main_hrun',
    #     'schedule': crontab(),
    #     'args': ()
    # }
    #     'comment_views': {
    #         'task': 'blog.tasks.comment.test1',
    #         'schedule': crontab(minute='*/30'),
    #         'args': ()
    #     }
    # },

    # 是能能编辑自己创建开关
    "EDIT_SWITCH": False,

    "SERVICE_DIR": ""
}
