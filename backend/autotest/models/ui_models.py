import typing

from sqlalchemy import String, Integer, JSON, select, func, Text, DateTime, text, DECIMAL
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.models.base import Base
from autotest.models.system_models import User, FileInfo
from autotest.schemas.ui.ui_case import UiCaseQuery
from autotest.schemas.ui.ui_element import UiElementQuery
from autotest.schemas.ui.ui_page import UiPageQuery
from autotest.schemas.ui.ui_report import UiReportQuery, UiReportDetailQuery


class UiPage(Base):
    """页面表"""
    __tablename__ = 'ui_page'

    name = mapped_column(String(255), nullable=False, comment='页面名称', index=True)
    url = mapped_column(String(255), comment='url')
    project_id = mapped_column(Integer, comment='项目id')
    module_id = mapped_column(Integer, comment='模块id')
    tags = mapped_column(JSON, comment='标签')
    remarks = mapped_column(String(255), comment='备注')

    @classmethod
    async def get_list(cls, params: UiPageQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.url:
            q.append(cls.url.like('%{}%'.format(params.url)))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      ModuleInfo.name.label('module_name'),
                      ProjectInfo.name.label('project_name'),
                      u.nickname.label('updated_by_name'),
                      func.count(UiElement.id).label('element_count'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(UiElement, UiElement.page_id == cls.id) \
            .group_by(cls.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_page_by_id(cls, id):
        q = [cls.enabled_flag == 1, cls.id == id]
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      ModuleInfo.name.label('module_name'),
                      ProjectInfo.name.label('project_name'),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())

        return await cls.get_result(stmt, first=True)


class UiElement(Base):
    """元素表"""
    __tablename__ = 'ui_element'

    name = mapped_column(String(255), nullable=False, comment='元素名称', index=True)
    location_method = mapped_column(String(255), comment='定位类型')
    location_value = mapped_column(String(255), comment='定位元素值')
    page_id = mapped_column(Integer, comment='关联页面', index=True)
    remarks = mapped_column(String(255), comment='备注')

    @classmethod
    async def get_list(cls, params: UiElementQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.page_id:
            q.append(cls.page_id == params.page_id)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_element_all(cls):
        q = [cls.enabled_flag == 1]
        stmt = select(cls.get_table_columns(),
                      UiPage.name.label('page_name'),
                      UiPage.id.label('page_id'),
                      UiPage.url.label('page_url'),
                      ) \
            .where(*q) \
            .outerjoin(UiPage, UiPage.id == cls.page_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)


class UiCase(Base):
    """ui 用例表"""
    __tablename__ = 'ui_case'

    name = mapped_column(String(255), nullable=False, comment='用例名', index=True)
    tags = mapped_column(JSON, comment='自动化标记')
    project_id = mapped_column(Integer, comment='项目id')
    module_id = mapped_column(Integer, comment='模块id')
    steps = mapped_column(JSON, comment='运行步骤')
    setup_hooks = mapped_column(JSON, comment='前置操作')
    teardown_hooks = mapped_column(JSON, comment='后置操作')
    variables = mapped_column(JSON, comment='变量')
    version = mapped_column(String(255), comment='版本')
    remarks = mapped_column(String(255), comment='备注')

    @classmethod
    async def get_list(cls, params: UiCaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      ModuleInfo.name.label('module_name'),
                      ProjectInfo.name.label('project_name'),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_case_by_id(cls, id):
        q = [cls.enabled_flag == 1, cls.id == id]
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')
                      ) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)


class UiSteps(Base):
    """步骤表"""
    __tablename__ = 'ui_steps'

    index = mapped_column(String(255), nullable=False, comment='步骤排序', index=True)
    operation = mapped_column(String(255), comment='操作')
    input_data = mapped_column(String(255), comment='输入数据')
    location_method = mapped_column(String(255), comment='定位元素方式')
    location_value = mapped_column(String(255), comment='定位元素值')
    output = mapped_column(String(255), comment='输出')
    remarks = mapped_column(String(255), comment='备注')
    case_id = mapped_column(Integer, comment='关联ui测试用例')
    version = mapped_column(String(255), comment='版本')


class UiReports(Base):
    """报告表"""
    __tablename__ = 'ui_reports'

    name = mapped_column(String(255), nullable=False, comment='报告名', index=True)
    start_time = mapped_column(DateTime, comment='执行时间')
    duration = mapped_column(DECIMAL(), comment='执行耗时')
    case_id = mapped_column(Integer(), comment='用例id', index=True)
    run_mode = mapped_column(Integer, comment='运行类型， 10 同步， 20 异步，30 定时任务')
    success = mapped_column(Integer(), comment='是否成功')
    run_count = mapped_column(Integer, comment='运行步骤数')
    run_success_count = mapped_column(Integer, comment='运行成功数')
    run_fail_count = mapped_column(Integer, comment='运行失败数')
    run_skip_count = mapped_column(Integer, comment='运行跳过数')
    run_err_count = mapped_column(Integer, comment='运行错误数')
    run_log = mapped_column(Text, comment='运行日志')
    project_id = mapped_column(String(255), comment='项目id')
    module_id = mapped_column(String(255), comment='模块id')
    env_id = mapped_column(Integer, comment='运行环境')
    exec_user_id = mapped_column(Integer, comment='执行人id')
    exec_user_name = mapped_column(String(255), comment='执行人昵称')

    @classmethod
    async def get_list(cls, params: UiReportQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.user_ids:
            q.append(cls.execute_user_id.in_(params.user_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.min_and_max:
            q.append(cls.creation_date.between(*params.min_and_max))
        if params.exec_user_name:
            q.append(cls.exec_user_name.like('%{}%'.format(params.exec_user_name)))
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    def get_project_by_name(cls, project_name):
        return cls.query.filter(cls.project_name == project_name, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_id(cls, report_id):
        return cls.query.filter(cls.id == report_id, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_time(cls, begin_time, end_time):
        return cls.query.filter(cls.enabled_flag == 1, cls.start_at.between(begin_time, end_time),
                                cls.success.isnot(None)) \
            .with_entities(cls.id,
                           cls.name,
                           cls.start_time,
                           cls.success,
                           cls.run_count,
                           cls.run_success_count,
                           cls.created_by,
                           cls.run_type,
                           cls.run_mode)

    @classmethod
    def statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.outerjoin(User, User.id == cls.execute_user_id) \
            .with_entities(
            func.count(cls.id).label('run_num'),
            User.username.label('employee_code'),
            User.nickname.label('username'),
        ) \
            .filter(cls.enabled_flag == 1,
                    cls.execute_user_id != -1,
                    *q)

    @classmethod
    def get_statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.filter(cls.enabled_flag == 1,
                                cls.execute_user_id != -1,
                                *q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .with_entities(
            cls.id,
            ProjectInfo.name.label('project_name'),
            func.round(func.sum(func.if_(cls.success, 1, 0)) / func.count(cls.id) * 100, 2).label(
                'pass_rate'),
            func.round(func.sum(cls.successful_use_case) / func.sum(cls.run_test_count) * 100, 2).label(
                'successes_rate'),
        ).group_by(text('project_name'))


class UiReportDetail:
    """报告表"""

    _mapper = {}

    @staticmethod
    def model(id: int):
        # 目前一个表，多个表修改取模数
        table_index = id % 1  # 取模数 100 代表 100 张表
        class_name = f'ui_report_detail_{table_index}'

        mode_class = UiReportDetail._mapper.get(class_name, None)
        if mode_class is None:
            class ModelClass(Base):
                __module__ = __name__
                __name__ = class_name,
                __tablename__ = class_name

                name = mapped_column(String(255), nullable=False, comment='报告名', index=True)
                index = mapped_column(String(255), comment='步骤顺序')
                variables = mapped_column(JSON, comment='步骤变量')
                data = mapped_column(String(500), comment='步骤数据')
                action = mapped_column(String(255), comment='步骤动作')
                location_method = mapped_column(String(255), comment='定位方式')
                location_value = mapped_column(String(255), comment='定位值')
                report_id = mapped_column(Integer, comment='报告id', index=True)
                success = mapped_column(Integer(), comment='是否成功')
                status = mapped_column(String(255), comment='状态')
                case_id = mapped_column(Integer(), comment='用例id', index=True)
                step_id = mapped_column(Integer(), comment='步骤id', index=True)
                remarks = mapped_column(String(255), comment='备注')
                start_time = mapped_column(DateTime, comment='开始时间')
                duration = mapped_column(DECIMAL(), comment='耗时')
                setup_hook_results = mapped_column(JSON, comment='前置hook结果')
                teardown_hook_results = mapped_column(JSON, comment='后置hook结果')
                validator_results = mapped_column(JSON, comment='断言结果')
                screenshot_file_id = mapped_column(String(255), comment='截图文件id')
                log = mapped_column(Text, comment='运行日志')
                message = mapped_column(Text, comment='运行信息')

                @classmethod
                async def get_list(cls, params: UiReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.report_id)
                    if params.name:
                        q.append(cls.name.like(f"%{params.name}%"))
                    if params.step_type:
                        q.append(cls.step_type == params.step_type)
                    if params.status_list:
                        q.append(cls.status.in_(params.status_list))

                    stmt = select(cls.get_table_columns(),
                                  User.nickname.label('case_created_by_name'), ).where(*q) \
                        .outerjoin(User, User.id == cls.created_by) \
                        .order_by(cls.index)
                    return await cls.pagination(stmt)

                @classmethod
                async def get_details(cls, params: UiReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.report_id)
                    if params.name:
                        q.append(cls.name.like(f"%{params.name}%"))
                    if params.step_type:
                        q.append(cls.step_type == params.step_type)
                    if params.status_list:
                        q.append(cls.status.in_(params.status_list))

                    stmt = select(cls.get_table_columns(),
                                  User.nickname.label('case_created_by_name'),
                                  func.concat('static/', 'files/', FileInfo.name).label("screenshot_url"),
                                  ).where(*q) \
                        .outerjoin(User, User.id == cls.created_by) \
                        .outerjoin(FileInfo, FileInfo.id == cls.screenshot_file_id) \
                        .order_by(cls.index)
                    return await cls.get_result(stmt)

                @classmethod
                async def statistics(cls, params: UiReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.report_id)

                    stmt = select(
                        # 总步骤数
                        func.count('1').label("count_step"),
                        # 成功步骤数
                        func.sum(func.if_(cls.status == "SUCCESS" == 1, 1, 0)).label("count_step_success"),
                        # 失败步骤数
                        func.sum(func.if_(cls.status == "FAILURE" == 1, 1, 0)).label("count_step_failure"),
                        # 跳过步骤数
                        func.sum(func.if_(cls.status == "SKIP" == 1, 1, 0)).label("count_step_skip"),
                        # 错误步骤数
                        func.sum(func.if_(cls.status == "ERROR" == 1, 1, 0)).label("count_step_error"),
                        # 总执行时长
                        func.sum(cls.duration).label("count_request_time"),
                        # 用例数
                        func.sum(func.if_(cls.status != "SKIP", 1, 0)).label("count_case"),
                        # 成功用例数
                        func.sum(func.if_(cls.status == "SUCCESS", 1, 0)).label("count_case_success"),
                        # 失败用例数
                        func.sum(func.if_(cls.status == "FAILURE", 1, 0)).label("count_case_fail"),
                        # 测试用例通过率
                        func.round(
                            func.sum(
                                func.if_(cls.status == "SUCCESS", func.if_(cls.status != "SKIP", 1, 0), 0)) / func.sum(
                                func.if_(cls.status != "SKIP", 1, 0)) * 100, 2).label(
                            "case_pass_rate"),
                        # 测试步骤通过率
                        func.round(func.sum(func.if_(cls.status == "SUCCESS", 1, 0)) / func.count('1') * 100, 2).label(
                            "step_pass_rate")).where(*q)

                    return await cls.get_result(stmt, first=True)

            mode_class = ModelClass
            UiReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls
