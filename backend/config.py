# -*- coding: utf-8 -*-
# @author: xiaobai
import os
import typing
from pathlib import Path

from pydantic import AnyHttpUrl, Field, BaseSettings

project_banner = """
███████╗███████╗██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗██████╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝██╔══██╗
  ███╔╝ █████╗  ██████╔╝██║   ██║██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""
__version__ = "2.1.5"

project_desc = """
    🎉 zerorunner 管理员接口汇总 🎉
"""


class Configs(BaseSettings):
    PROJECT_DESC: str = project_desc  # 描述
    PROJECT_BANNER: str = project_banner  # 描述
    PROJECT_VERSION: typing.Union[int, str] = __version__  # 版本
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8100"  # 开发环境

    API_PREFIX: str = "/api"  # 接口前缀
    STATIC_DIR: str = 'static'  # 静态文件目录
    GLOBAL_ENCODING: str = 'utf8'  # 全局编码
    CORS_ORIGINS: typing.List[typing.Any] = ["*"]  # 跨域请求
    WHITE_ROUTER: list = ["/api/user/login", "/api/file"]  # 路由白名单，不需要鉴权

    SECRET_KEY: str = "kPBDjVk0o3Y1wLxdODxBpjwEjo7-Euegg4kdnzFIRjc"  # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token过期时间: 60 minutes * 24 hours * 1 days = 1 days

    # redis
    REDIS_URI: str = Field(..., env="REDIS_URI")  # redis

    # DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db?check_same_thread=False"  # Sqlite(异步)
    DATABASE_URI: str = Field(..., env="MYSQL_DATABASE_URI")  # MySQL(异步)
    # DATABASE_URI: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"  # PostgreSQL(异步)
    DATABASE_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)

    # logger
    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = 'zerorunner.log'  # 日志文件名  (时间格式 {time:YYYY-MM-DD_HH-mm-ss}.log)
    LOGGER_LEVEL: str = 'INFO'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "10 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    # dir
    BASEDIR: str = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

    # celery worker
    broker_url: str = Field(..., env="CELERY_BROKER_URL")
    # result_backend: str = Field(..., env="CELERY_RESULT_BACKEND")
    task_serializer: str = "pickle"
    result_serializer: str = "pickle"
    accept_content: typing.Tuple = ("pickle", "json",)
    task_protocol: int = 2
    timezone: str = "Asia/Shanghai"
    enable_utc: bool = False
    broker_connection_retry_on_startup: bool = True
    # 并发工作进程/线程/绿色线程执行任务的数量 默认10
    worker_concurrency: int = 10
    # 一次预取多少消息乘以并发进程数 默认4
    worker_prefetch_multiplier: int = 4
    # 池工作进程在被新任务替换之前可以执行的最大任务数。默认是没有限制
    worker_max_tasks_per_child: int = 100
    # 连接池中可以打开的最大连接数 默认10
    broker_pool_limit: int = 10
    # 传递给底层传输的附加选项的字典。设置可见性超时的示例（Redis 和 SQS 传输支持）
    result_backend_transport_options: typing.Dict[str, typing.Any] = {'visibility_timeout': 3600}
    worker_cancel_long_running_tasks_on_connection_loss: bool = True
    include: typing.List[str] = [
        'celery_worker.tasks.test_case',
        'celery_worker.tasks.common',
        'celery_worker.tasks.task_run',
        'celery_worker.tasks.ui_case',
    ]
    # task_queues = (
    #     Queue('default', routing_key='default'),
    #     Queue('ui_case', routing_key='ui_case'),
    #     Queue('api_case', routing_key='api_case'),
    # )

    #  job -A your_app worker -Q api_case,ui_case

    TEST_FILES_DIR: str = Path(__file__).parent.joinpath("static", "files").as_posix()
    PROJECT_ROOT_DIR: str = Path(__file__).parent.as_posix()

    task_run_pool: int = 3

    # job beat
    beat_db_uri: str = Field(..., env="CELERY_BEAT_DB_URL")

    # jacoco service
    JACOCO_SERVER_URL: str = Field(None, env="JACOCO_SERVER_URL")

    # gitlab
    GITLAB_URL: str = Field(None, env="GITLAB_URL")
    GITLAB_TOKEN: str = Field(None, env="GITLAB_TOKEN")
    GITLAB_USER: str = Field(None, env="GITLAB_USER_ID")
    GITLAB_PASSWORD: str = Field(None, env="GITLAB_PASSWORD")

    class Config:
        case_sensitive = True  # 区分大小写
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Configs()
