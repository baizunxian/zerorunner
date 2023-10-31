import typing

from pydantic import root_validator, Field

from autotest.schemas.base import BaseSchema


class TimedTasksQuerySchema(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List[typing.Union[int, str]] = Field(None, description="ids")
    name: str = Field(None, description="")
    created_by_name: str = Field(None, description="")
    created_by: int = Field(None, description="")
    user_ids: typing.List[typing.Union[int, str]] = Field(None, description="")
    project_ids: typing.List[typing.Union[int, str]] = Field(None, description="")


class TimedTasksListSchema(BaseSchema):
    name: str = Field(None, description="")
    task: str = Field(None, description="")
    args: str = Field(None, description="")
    kwargs: str = Field(None, description="")
    queue: str = Field(None, description="")
    exchange: str = Field(None, description="")
    routing_key: str = Field(None, description="")
    enabled: int = Field(None, description="")
    total_run_count: int = Field(None, description="")
    description: str = Field(None, description="")
    crontab_id: int = Field(None, description="")
    crontab_str: str = Field(None, description="")
    interval_id: int = Field(None, description="")
    run_type: str = Field(None, description="")
    project_id: int = Field(None, description="")
    project_name: str = Field(None, description="")
    module_id: int = Field(None, description="")
    module_name: str = Field(None, description="")
    suite_id: int = Field(None, description="")
    case_ids: str = Field(None, description="")
    expires: str = Field(None, description="")
    last_run_at: str = Field(None, description="")
    date_changed: str = Field(None, description="")


class CrontabSaveSchema(BaseSchema):
    """Crontab"""

    crontab: str = Field(None, description="")


class IntervalIn(BaseSchema):
    """Crontab"""

    every: int = Field(..., description="")
    period: str = Field(..., description="")


class TimedTasksInSchema(BaseSchema):
    """定时任务保存更新"""
    id: int = Field(None, description="")
    case_ids: typing.List[typing.Union[int, str]] = Field(None, description="用例id")
    case_env_id: int = Field(None, description="case 环境id")
    ui_ids: typing.List[typing.Union[int, str]] = Field(None, description="ui用例id")
    ui_env_id: int = Field(None, description="ui case 环境id")
    script_ids: typing.List[typing.Union[int, str]] = Field(None, description="脚本id")
    module_id: int = Field(None, description="")
    project_id: int = Field(None, description="")
    run_mode: str = Field(None, description="")
    crontab: str = Field(None, description="")
    module_ids: str = Field(None, description="")
    name: str = Field(..., description="")
    task: str = Field(None, description="")
    description: str = Field(None, description="")
    kwargs: str = Field(None, description="执行参数")
    crontab_id: int = Field(None, description="执行参数")
    task_type: str = Field(None, description="任务类型， crontab or interval")
    interval_id: int = Field(None, description="区间id")
    interval_every: int = Field(None, description="区间数")
    interval_period: str = Field(None, description="间隔单位")
    task_tags: typing.List[str] = Field(None, description="任务标签")
    remarks: int = Field(None, description="备注")


class TimedTasksId(BaseSchema):
    """"""
    id: int = Field(..., description="")


class TaskKwargsIn(BaseSchema):
    """定时任务执行参数"""
    case_ids: typing.List[typing.Union[str, int]] = Field(None, description="ids")
    case_env_id: int = Field(None, description="环境id")
    ui_ids: typing.List[typing.Union[str, int]] = Field(None, description="ids")
    ui_env_id: int = Field(None, description="环境id")
    name: str = Field(None, description="任务名称")
    project_id: int = Field(None, description="项目id")
    run_type: str = Field(None, description="运行类型")
    run_mode: int = Field(None, description="10同步 20异步 30定时任务")
    env_id: int = Field(None, description="环境id")
    exec_user_id: int = Field(None, description="执行人id")
    exec_user_name: str = Field(None, description="执行人名称")


class TimedTaskCaseQuery(BaseSchema):
    task_id: int = Field(..., description="任务id")
    type: str = Field(..., description="类型")
