# -*- coding: utf-8 -*-
# @author: xiaobai
import datetime as dt
import typing

from sqlalchemy import Integer, String, DateTime, Boolean, insert, update, select, Text, func, BigInteger
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.api_models import ModuleInfo, ProjectInfo, ApiCase
from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.api.timed_task import TimedTasksQuerySchema, TimedTasksId, TimedTaskCaseQuery
from autotest.schemas.job.task_record import TaskRecordQuery


class TimedTask(Base):
    """定时任务表"""
    __tablename__ = 'celery_periodic_task'

    name = mapped_column(String(200), nullable=False, comment='定时任务名')
    task = mapped_column(String(200), comment='任务路径')
    args = mapped_column(String(200), comment='参数')
    kwargs = mapped_column(String(200), comment='关键字参数')
    queue = mapped_column(String(200), comment='队列')
    exchange = mapped_column(String(200), comment='交换')
    routing_key = mapped_column(String(200), comment='路由密钥')
    expires = mapped_column(DateTime, comment='到期时间')
    one_off = mapped_column(Boolean, comment='执行一次')
    start_time = mapped_column(DateTime, comment='开始时间')
    enabled = mapped_column(String(200), comment='是否启用, 1启动，0停用', default=0)
    last_run_at = mapped_column(String(200), comment='上次运行时间')
    total_run_count = mapped_column(String(200), comment='运行总次数', default=0)
    date_changed = mapped_column(DateTime, comment='更改日期')
    description = mapped_column(String(200), comment='备注')
    crontab_id = mapped_column(Integer, comment='定时器id')
    crontab = mapped_column(Integer, comment='crontab 表达式')
    interval_id = mapped_column(Integer, comment='间隔id')
    interval_every = mapped_column(Integer, comment='间隔时间')
    interval_period = mapped_column(String(24), comment='间隔类型')
    task_type = mapped_column(String(255), nullable=False, comment="crontab interval")
    project_id = mapped_column(BigInteger, nullable=True, comment='项目id')
    module_id = mapped_column(BigInteger, nullable=False, comment='模块id')
    suite_id = mapped_column(Integer, nullable=False, comment='套件id')
    case_env_id = mapped_column(BigInteger, nullable=False, comment='case_env_id 用例环境')
    case_ids = mapped_column(String(255), nullable=False, comment='用例集合')
    ui_env_id = mapped_column(BigInteger, nullable=False, comment='case_env_id 用例环境')
    ui_ids = mapped_column(String(255), nullable=False, comment='ui用例集合')
    script_ids = mapped_column(String(255), nullable=False, comment='脚本id')
    task_tags = mapped_column(String(255), nullable=False, comment='任务标签')
    remarks = mapped_column(String(255), nullable=False, comment='任务描述')

    @classmethod
    async def get_list(cls, params: TimedTasksQuerySchema):
        q = [cls.enabled_flag == 1]
        u = aliased(User)
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(u.nickname.like('%{}%'.format(params.created_by_name)))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))

        stmt = select(cls).where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .with_only_columns(cls.get_table_columns(),
                               u.nickname.label('created_by_name'),
                               User.nickname.label('updated_by_name'),
                               ProjectInfo.name.label('project_name'),
                               ModuleInfo.name.label('module_name')) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_timed_task_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_task_by_name(cls, name):
        """获取任务名存在的个数"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)


class TimedTaskCase(Base):
    """定时任务用例关联表"""
    __tablename__ = 'timed_task_case'

    task_id = mapped_column(BigInteger(), nullable=False, comment='定时任务id')
    case_id = mapped_column(BigInteger(), nullable=False, comment='关系id')
    type = mapped_column(String(255), nullable=False, comment='类型, case, ui, script, api')

    @classmethod
    async def get_by_case(cls, params: TimedTaskCaseQuery):
        stmt = (select(cls.id.label("r_id"),
                       TimedTask.id.label("task_id"),
                       ApiCase.id.label("id"),
                       ApiCase.name.label("name"),
                       ApiCase.remarks.label("remarks"),
                       ApiCase.creation_date.label("creation_date"),
                       User.nickname.label("created_by_name"),
                       )
        .outerjoin(TimedTask, TimedTask.id == cls.task_id)
        .outerjoin(ApiCase, ApiCase.id == cls.case_id)
        .outerjoin(User, User.id == ApiCase.created_by)
        .where(cls.task_id == params.task_id, cls.type == "case", cls.enabled_flag == 1).order_by(
            cls.id.desc()))
        return await cls.get_result(stmt)

    @classmethod
    async def get_relation_by_case_ids(cls, ids: typing.List):
        stmt = (select(cls.id.label("r_id"),
                       TimedTask.id.label("id"),
                       func.concat("timed_task_", TimedTask.id).label("relation_id"),
                       func.concat("case_", ApiCase.id).label("from_relation_id"),
                       func.concat("timed_task_", TimedTask.id).label("to_relation_id"),
                       TimedTask.name.label("name"),
                       ApiCase.id.label("case_id"),
                       ApiCase.name.label("case_name"),
                       ApiCase.remarks.label("remarks"),
                       TimedTask.creation_date.label("creation_date"),
                       User.nickname.label("created_by_name")
                       ).outerjoin(TimedTask, TimedTask.id == cls.task_id)
        .outerjoin(ApiCase, ApiCase.id == cls.case_id)
        .outerjoin(User, User.id == TimedTask.created_by)
        .where(cls.case_id.in_(ids), cls.type == "case", cls.enabled_flag == 1).order_by(
            cls.id.desc()))
        return await cls.get_result(stmt)

    @classmethod
    async def get_relation_by_timed_task_ids(cls, ids: typing.List):
        stmt = (select(func.any_value(cls.id).label("r_id"),
                       func.any_value(TimedTask.id).label("timed_task_id"),
                       func.any_value(ApiCase.id).label("id"),
                       func.any_value(ApiCase.name).label("name"),
                       func.any_value(func.concat("case_", ApiCase.id)).label("relation_id"),
                       func.any_value(func.concat("case_", ApiCase.id)).label("from_relation_id"),
                       func.any_value(func.concat("timed_task_", TimedTask.id)).label("to_relation_id"),
                       func.any_value(ApiCase.creation_date).label("creation_date"),
                       func.any_value(User.nickname).label("created_by_name"),
                       )
                .outerjoin(TimedTask, TimedTask.id == cls.task_id)
                .outerjoin(ApiCase, ApiCase.id == cls.case_id)
                .outerjoin(User, User.id == TimedTask.created_by)
                .where(cls.task_id.in_(ids), cls.type == "case", cls.enabled_flag == 1)
                .order_by(cls.id.desc()))
        return await cls.get_result(stmt)

    @classmethod
    async def deleted_by_task_id(cls, task_id):
        """删除定时任务用例关联表"""
        stmt = update(cls).where(cls.task_id == task_id).values(enabled_flag=0)
        await cls.execute(stmt)


class Crontab(Base):
    """crontab 表"""
    __tablename__ = 'celery_crontab_schedule'

    id = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    minute = mapped_column(String(200), comment='分钟')
    hour = mapped_column(String(200), comment='小时')
    day_of_week = mapped_column(String(200), comment='日期')
    day_of_month = mapped_column(String(200), comment='月份')
    month_of_year = mapped_column(String(200), comment='年')
    timezone = mapped_column(String(200), comment='时区', default='Asia/Shanghai')

    @classmethod
    async def get_crontab_by_parameter(cls, minute, hour, day_of_week, day_of_month, month_of_year):
        stmt = select(cls).where(cls.minute == minute, cls.hour == hour, cls.day_of_week == day_of_week,
                                 cls.day_of_month == day_of_month, cls.month_of_year == month_of_year)
        return await cls.get_result(stmt, first=True)


class IntervalSchedule(Base):
    """时间间隔 表"""
    __tablename__ = 'celery_interval_schedule'

    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    MICROSECONDS = 'microseconds'

    id = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    every = mapped_column(Integer, comment='区间数')
    period = mapped_column(String(24), comment='间隔单位')

    @classmethod
    async def get_interval_by_parameter(cls, every, period):
        stmt = select(cls).where(cls.every == every, cls.period == period)
        return await cls.get_result(stmt, first=True)


class PeriodicTaskChanged(Base):
    """定时任务更新表"""
    __tablename__ = 'celery_periodic_task_changed'

    id = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    last_update = mapped_column(DateTime, comment='到期时间')

    @classmethod
    async def update_changed(cls):
        stmt = select(cls).where(cls.id == 1).limit(1)
        s = await cls.get_result(stmt, first=True)
        if s:
            stmt = update(cls).where(cls.id == 1).values(last_update=dt.datetime.now())
        else:
            stmt = insert(cls).values(id=1, last_update=dt.datetime.now())
        await cls.execute(stmt)


# 任务记录表
class CeleryTaskRecord(Base):
    __tablename__ = 'celery_task_record'

    id = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    task_id = mapped_column(String(255), nullable=False, comment='任务id')
    task_name = mapped_column(String(255), nullable=False, comment='任务名称')
    task_type = mapped_column(String(255), nullable=False, comment='任务类型 10普通任务 20定时任务')
    status = mapped_column(String(255), nullable=False, comment='任务状态')
    result = mapped_column(String(255), nullable=False, comment='任务结果')
    start_time = mapped_column(DateTime, nullable=False, comment='开始时间')
    end_time = mapped_column(DateTime, nullable=False, comment='结束时间')
    duration = mapped_column(String(255), nullable=False, comment='耗时')
    traceback = mapped_column(Text, nullable=False, comment='异常信息')
    business_id = mapped_column(BigInteger(), nullable=False, comment='业务id')
    args = mapped_column(Text, nullable=False, comment='业务参数')
    kwargs = mapped_column(Text, nullable=False, comment='业务参数')

    @classmethod
    async def get_list(cls, params: TaskRecordQuery):
        q = [cls.enabled_flag == 1]
        if params.task_name:
            q.append(cls.task_name.like('%{}%'.format(params.task_name)))
        if params.task_type:
            q.append(cls.task_type == params.task_type)
        if params.status:
            q.append(cls.status == params.status)
        if params.start_time:
            q.append(cls.start_time >= params.start_time)
        if params.end_time:
            q.append(cls.end_time <= params.end_time)
        if params.task_id:
            q.append(cls.task_id == params.task_id)
        if params.trace_id:
            q.append(cls.trace_id == params.trace_id)
        if params.business_id:
            q.append(cls.business_id == params.business_id)
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_task_record_by_task_id(cls, task_id: str) -> dict:
        stmt = select(cls.get_table_columns()).where(cls.task_id == task_id)
        return await cls.get_result(stmt, first=True)
