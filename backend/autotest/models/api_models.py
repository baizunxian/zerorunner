import typing
from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, func, \
    distinct, text, and_, JSON, DECIMAL, select, update
from sqlalchemy.orm import aliased

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.api.api_case import ApiCaseQuery
from autotest.schemas.api.api_info import ApiQuery
from autotest.schemas.api.data_source import SourceQuery
from autotest.schemas.api.env import EnvQuery, BindingDataSourceIn, BindingFuncIn
from autotest.schemas.api.functions import FuncQuery
from autotest.schemas.api.module import ModuleQuery
from autotest.schemas.api.projectquery import ProjectQuery
from autotest.schemas.api.test_report import TestReportQuery, TestReportDetailQuery


class ProjectInfo(Base):
    """项目表"""
    __tablename__ = 'project_info'

    name = Column(String(64), nullable=False, comment='项目名称', index=True)
    responsible_name = Column(String(64), nullable=False, comment='负责人')
    test_user = Column(String(100), nullable=False, comment='测试人员')
    dev_user = Column(String(100), nullable=False, comment='开发人员')
    publish_app = Column(String(100), nullable=False, comment='发布应用')
    simple_desc = Column(String(100), nullable=True, comment='简要描述')
    remarks = Column(String(100), nullable=True, comment='其他信息')
    config_id = Column(Integer, nullable=True, comment='关联配置id')
    product_id = Column(Integer, nullable=True, comment='产品线id')

    @classmethod
    async def get_list(cls, params: ProjectQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.id:
            q.append(cls.id == params.id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .join(u, u.id == cls.updated_by) \
            .join(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_project_by_id(cls, id: int):
        stmt = select(cls.get_table_columns()).where(cls.id == id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_project_id_list(cls):
        return cls.query.filter(cls.enabled_flag == 1) \
            .with_entities(cls.id,
                           cls.responsible_name,
                           cls.test_user,
                           cls.dev_user,
                           cls.created_by) \
            .all()

    @classmethod
    async def get_project_by_name(cls, name):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_project_ids(cls):
        return cls.query.filter(cls.enabled_flag == 1).with_entities(cls.id).all()

    @classmethod
    def get_project_by_product_id(cls, product_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.product_id == product_id).with_entities(cls.id).all()


class ModuleInfo(Base):
    """模块表"""
    __tablename__ = 'module_info'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True, index=True)

    name = Column(String(64), nullable=False, comment='模块名称', index=True)
    project_id = Column(Integer, nullable=False, comment='归属项目id')
    config_id = Column(Integer, nullable=True, comment='关联配置id')
    test_user = Column(String(100), nullable=False, comment='测试负责人')
    simple_desc = Column(String(100), nullable=False, comment='简要描述')
    remarks = Column(String(100), nullable=False, comment='其他信息')
    module_packages = Column(String(64), nullable=False, comment='模块对应的包名称', index=True)
    leader_user = Column(String(100), nullable=False, comment='负责人')
    priority = Column(Integer, nullable=False, comment='默认执行用例优先级', default=4)

    # packages_id = Column(Integer, nullable=False, comment='包id')

    @classmethod
    async def get_list(cls, params: ModuleQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.project_name:
            q.append(ProjectInfo.project_name.like('%{}%'.format(params.project_name)))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        # if packages_id:
        #     q.append(cls.packages_id == packages_id)
        if params.sort_type == 0:
            sort_type = 'asc'
        else:
            sort_type = 'desc'
        if not params.order_field or params.order_field == 'creation_date':
            params.order_field = 'module_info.creation_date'
        if params.order_field == 'project_name':
            params.order_field = 'project_info.name'
        if params.order_field == 'test_user':
            params.order_field = 'user.nickname'
        order_by = '{} {} {} {}'.format(params.order_field, sort_type, ',module_info.id', sort_type)
        u = aliased(User)

        stmt = select(cls.get_table_columns(),
                      func.count(distinct(ApiInfo.id)).label('case_count'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name')).where(*q) \
            .join(ProjectInfo, and_(cls.project_id == ProjectInfo.id, ProjectInfo.enabled_flag == 1)) \
            .join(User, User.id == cls.created_by) \
            .join(u, u.id == cls.updated_by) \
            .outerjoin(ApiInfo, and_(cls.id == ApiInfo.module_id, ApiInfo.enabled_flag == 1)) \
            .group_by(cls.id).order_by(text(order_by))
        return await cls.pagination(stmt)

    @classmethod
    async def get_module_by_project_id(cls, project_id: int):
        """查询项目是否有关联模块"""
        stmt = select(cls.id).where(cls.project_id == project_id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_module_by_name(cls, name: str):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_module_by_id(cls, id):
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    def get_module_by_module_packages(cls, module_packages):
        return cls.query.filter(cls.module_packages == module_packages, cls.enabled_flag == 1).all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_module_by_packages_id(cls, packages_id):
        return cls.query.filter(cls.packages_id == packages_id, cls.enabled_flag == 1).first()


class ApiInfo(Base):
    """接口用例"""
    __tablename__ = 'api_info'

    name = Column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    module_id = Column(Integer, nullable=False, comment='所属模块')
    status = Column(Integer, nullable=True, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code_id = Column(BigInteger, nullable=True, comment='关联接口id')
    code = Column(String(255), nullable=True, comment='接口code')
    priority = Column(Integer, nullable=False, comment='优先级', default=3)
    tags = Column(JSON, nullable=True, comment='用例标签')
    url = Column(JSON, nullable=True, comment='请求地址')
    method = Column(String(255), nullable=True, comment='请求方式')
    remarks = Column(String(255), nullable=True, comment='描述')
    step_type = Column(String(255), nullable=True, comment='描述')
    pre_steps = Column(JSON, nullable=True, comment='前置步骤')
    post_steps = Column(JSON, nullable=True, comment='后置步骤')
    setup_code = Column(JSON, nullable=True, comment='前置code')
    teardown_code = Column(JSON, nullable=True, comment='后置code')
    setup_hooks = Column(JSON, nullable=True, comment='前置操作')
    teardown_hooks = Column(JSON, nullable=True, comment='后置操作')
    headers = Column(JSON, nullable=True, comment='请求头')
    variables = Column(JSON, nullable=True, comment='变量')
    validators = Column(JSON, nullable=True, comment='断言规则')
    extracts = Column(JSON, nullable=True, comment='提取')
    export = Column(JSON, nullable=True, comment='输出')
    request = Column(JSON, nullable=True, comment='请求参数')
    sql_request = Column(JSON, nullable=True, comment='sql请求参数')
    loop_data = Column(JSON, nullable=True, comment='sql请求参数')
    if_data = Column(JSON, nullable=True, comment='sql请求参数')
    wait_data = Column(JSON, nullable=True, comment='sql请求参数')

    @classmethod
    async def get_list(cls, params: ApiQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.module_ids:
            q.append(cls.module_id.in_(params.module_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.priority:
            q.append(cls.priority.in_(params.priority))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.api_status:
            q.append(cls.api_status == params.api_status)
        u = aliased(User)

        sort_type = 'asc' if params.sort_type == 0 else 'desc'

        if not params.order_field or params.order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        elif params.order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        elif params.order_field == 'name':
            order_field = 'api_info.name'
        elif params.order_field == 'project_name':
            order_field = 'project_info.name'
        elif params.order_field == 'module_name':
            order_field = 'module_info.name'
        elif params.order_field == 'created_by_name' or params.order_field == 'updated_by_name':
            order_field = 'user.nickname'
        else:
            order_field = 'api_info.id'
        order_by = f'{order_field} {sort_type}'

        stmt = select(cls.id,
                      cls.name,
                      cls.url,
                      cls.method,
                      cls.project_id,
                      cls.module_id,
                      cls.code_id,
                      cls.code,
                      cls.priority,
                      cls.status,
                      cls.tags,
                      cls.updated_by,
                      cls.created_by,
                      cls.updation_date,
                      cls.creation_date,
                      cls.enabled_flag,
                      ProjectInfo.name.label('project_name'),
                      ModuleInfo.name.label('module_name'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')).where(*q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .order_by(text(order_by))

        return await cls.pagination(stmt)

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.enabled_flag == 1, cls.type == 1).all()

    @classmethod
    async def get_api_by_module_id(cls, module_id=None, module_ids=None):
        """查询模块是否有case关联"""
        q = [cls.enabled_flag == 1]
        if module_id:
            q.append(cls.module_id == module_id)
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_api_by_project_id(cls, project_id):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1)

    @classmethod
    async def get_api_by_name(cls, name):
        """获取用例名是否存在"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1, cls.name == name)
        return await cls.get_result(stmt)

    @classmethod
    def get_api_by_ids(cls, ids: typing.List[typing.Union[int, str]]):
        q = []
        return cls.query.filter(cls.id.in_(ids), *q, cls.enabled_flag == 1)

    @classmethod
    async def get_api_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    def get_api_by_time(cls, start_time, end_time):
        return cls.query.filter(cls.creation_date.between(start_time, end_time), cls.enabled_flag == 1)

    @classmethod
    def statistic_project_api_number(cls):
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectInfo.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)

    @classmethod
    def get_api_by_project_id_or_body(cls, project_id, body_name):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.request.like(('%{}%'.format(body_name))),
                                cls.enabled_flag == 1) \
            .with_entities(cls.id) \
            .all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()


class ApiCase(Base):
    """测试用例，集合"""
    __tablename__ = 'api_case'

    name = Column(String(64), nullable=False, comment='名称', index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    remarks = Column(String(255), nullable=False, comment='备注')
    headers = Column(JSON, nullable=False, comment='场景请求头')
    variables = Column(JSON, nullable=False, comment='场景变量')
    step_data = Column(JSON, nullable=False, comment='场景步骤')
    step_rely = Column(Integer, nullable=False, comment='步骤依赖  1依赖， 0 不依赖')

    # todo 目前步骤详情都冗余在单表，后面会拆为独立的表管理

    @classmethod
    async def get_list(cls, params: ApiCaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.created_by:
            q.append(User.nickname.like(f'%{params.created_by}%'))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by_name:
            q.append(User.nickname.like(f'%{params.created_by_name}%'))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)

        stmt = select(cls.id,
                      cls.name,
                      cls.project_id,
                      cls.remarks,
                      cls.created_by,
                      cls.creation_date,
                      cls.updated_by,
                      cls.updation_date,
                      cls.enabled_flag,
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name')).where(*q) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    def get_case_by_id(cls, id):
        """根据套件id查询用例"""
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    async def get_case_by_ids(cls, ids: typing.List[int]):
        """根据套件ids查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_case_by_name(cls, name: str):
        """根据套件名称查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    def statistic_project_case_number(cls):
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectInfo.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()


class ApiCaseStep(Base):
    """用例步骤"""
    __tablename__ = 'api_case_step'

    name = Column(String(64), nullable=False, comment='名称', index=True)
    parent_id = Column(Integer, nullable=False, comment='父级id')
    suite_id = Column(Integer, nullable=False, comment='套件id')
    step_type = Column(String(255), nullable=False, comment='步骤类型')
    case_id = Column(Integer, nullable=False, comment='case_id')
    value = Column(JSON, nullable=False, comment='步骤参数')
    enable = Column(Integer, nullable=False, comment='是否生效')
    index = Column(Integer, nullable=False, comment='顺序')
    node_id = Column(String(255), nullable=False, comment='节点id')

    @classmethod
    def get_list(cls, name=None, user_ids=None, project_id=None, created_by=None, suite_type=None,
                 created_by_name=None, project_ids=None, ids=None):
        q = list()
        if name:
            q.append(cls.name.like(f'%{name}%'))
        if suite_type:
            q.append(cls.suite_type == suite_type)
        if project_id:
            q.append(cls.project_id == project_id)
        if created_by:
            q.append(User.nickname.like(f'%{created_by}%'))
        if user_ids:
            q.append(cls.created_by.in_(user_ids))
        if project_ids:
            q.append(cls.project_id.in_(project_ids))
        if created_by_name:
            q.append(User.nickname.like(f'%{created_by_name}%'))
        if ids:
            q.append(cls.id.in_(ids))
        u = aliased(User)
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .with_entities(cls.id,
                           cls.name,
                           cls.project_id,
                           cls.headers,
                           cls.variables,
                           cls.created_by,
                           cls.creation_date,
                           cls.updated_by,
                           cls.updation_date,
                           cls.enabled_flag,
                           User.nickname.label('created_by_name'),
                           u.nickname.label('updated_by_name'),
                           ProjectInfo.name.label('project_name')) \
            .order_by(cls.creation_date.desc())


class ApiTestReport(Base):
    """报告表"""
    __tablename__ = 'api_test_report'

    name = Column(String(255), nullable=False, comment='报告名称', index=True)
    start_time = Column(DateTime, nullable=True, comment='执行时间')
    duration = Column(String(255), nullable=True, comment='运行耗时')
    case_id = Column(Integer, nullable=True, comment='执行用例id')
    run_mode = Column(String(255), nullable=True, comment='运行模式， case 用例， suites 套件')
    run_type = Column(Integer, nullable=True, comment='运行类型， 10 同步， 20 异步，30 定时任务')
    success = Column(Integer, nullable=True, comment='是否成功， True, False')
    run_count = Column(Integer, nullable=True, comment='运行步骤数')
    actual_run_count = Column(Integer, nullable=True, comment='实际步骤数')
    run_success_count = Column(Integer, nullable=True, comment='运行成功数')
    run_fail_count = Column(Integer, nullable=True, comment='运行失败数')
    run_skip_count = Column(Integer, nullable=True, comment='运行跳过数')
    run_err_count = Column(Integer, nullable=True, comment='运行错误数')
    run_log = Column(Text, nullable=True, comment='运行日志')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    env_id = Column(Integer, nullable=True, comment='运行环境')

    @classmethod
    async def get_list(cls, params: TestReportQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.run_user_name:
            q.append(User.created_by.like('%{}%'.format(params.run_user_name)))
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
        if params.execute_user_name:
            q.append(User.nickname.like('%{}%'.format(params.execute_user_name)))
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('run_user_name')) \
            .where(*q) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
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


class ApiTestReportDetail:
    """报告表"""
    _mapper = {}

    @staticmethod
    def model(id: int):
        # 目前一个表，多个表修改取模数
        table_index = id % 1
        class_name = 'api_test_report_detail_%d' % table_index

        mode_class = ApiTestReportDetail._mapper.get(class_name, None)
        if mode_class is None:
            class ModelClass(Base):
                __module__ = __name__
                __name__ = class_name,
                __tablename__ = 'api_test_report_detail_%d' % table_index

                name = Column(String(255), nullable=False, comment='步骤名称', index=True)
                case_id = Column(String(255), nullable=True, comment='用例id')
                success = Column(Integer, nullable=True, comment='是否成功， True, False')
                status = Column(String(255), nullable=True, comment='步骤状态  success 成功  fail 失败  skip 跳过')
                step_id = Column(String(255), nullable=True, comment='步骤id')
                parent_step_id = Column(String(255), nullable=True, comment='父级步骤id')
                step_type = Column(String(255), nullable=True, comment='步骤类型')
                step_tag = Column(String(255), nullable=True, comment='步骤标签 pre 前置，post 后置，controller 控制器')
                message = Column(Text, nullable=True, comment='步骤信息')
                variables = Column(JSON, nullable=True, comment='步骤变量')
                env_variables = Column(JSON, nullable=True, comment='环境变量')
                case_variables = Column(JSON, nullable=True, comment='会话变量')
                session_data = Column(JSON, nullable=True, comment='请求会话数据')
                export_vars = Column(JSON, nullable=True, comment='导出变量')
                report_id = Column(Integer, nullable=True, comment='报告id', index=True)
                url = Column(String(255), nullable=True, comment='请求地址')
                method = Column(String(255), nullable=True, comment='请求方法')
                start_time = Column(DateTime, nullable=True, comment='开始时间')
                duration = Column(DECIMAL(), nullable=True, comment='耗时')
                pre_hook_data = Column(JSON, nullable=True, comment='前置步骤')
                post_hook_data = Column(JSON, nullable=True, comment='后置步骤')
                setup_hook_results = Column(JSON, nullable=True, comment='前置hook结果')
                teardown_hook_results = Column(JSON, nullable=True, comment='后置hook结果')
                index = Column(Integer, nullable=True, comment='顺序')
                status_code = Column(Integer, nullable=True, comment='顺序')
                response_time_ms = Column(DECIMAL(), nullable=True, comment='响应耗时')
                elapsed_ms = Column(DECIMAL(), nullable=True, comment='请求耗时')
                log = Column(Text, nullable=True, comment='运行日志')

                @classmethod
                async def get_list(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.id)
                    if params.name:
                        q.append(cls.name.like(f"%{params.name}%"))
                    if params.url:
                        q.append(cls.url.like(f"%{params.url}%"))
                    if params.api_name:
                        q.append(ApiInfo.name.like(f"%{params.api_name}%"))
                    if params.step_type:
                        q.append(cls.step_type == params.step_type)
                    if params.status_list:
                        q.append(cls.status.in_(params.status_list))
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)
                    else:
                        q.append(cls.parent_step_id == None)

                    stmt = select(cls.get_table_columns(),
                                  ApiInfo.name.label("case_name"),
                                  ApiInfo.created_by.label('case_created_by'),
                                  User.nickname.label('case_created_by_name'), ).where(*q) \
                        .outerjoin(ApiInfo, ApiInfo.id == cls.case_id) \
                        .outerjoin(User, User.id == ApiInfo.created_by) \
                        .order_by(cls.index)
                    return await cls.pagination(stmt)

                @classmethod
                async def statistics(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.id)
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)
                    else:
                        q.append(cls.parent_step_id == None)

                    stmt = select(
                        # 总步骤数
                        func.count('1').label("count_step"),
                        # 成功步骤数
                        func.sum(func.if_(cls.status == "SUCCESS" == 1, 1, 0)).label(
                            "count_step_success"),
                        # 失败步骤数
                        func.sum(func.if_(cls.status == "FAILURE" == 1, 1, 0)).label(
                            "count_step_failure"),
                        # 跳过步骤数
                        func.sum(func.if_(cls.status == "SKIP" == 1, 1, 0)).label("count_step_skip"),
                        # 错误步骤数
                        func.sum(func.if_(cls.status == "ERROR" == 1, 1, 0)).label("count_step_error"),
                        # 平均请求时长
                        func.avg(cls.elapsed_ms).label("avg_request_time"),
                        # 总执行时长
                        func.sum(cls.duration).label("count_request_time"),
                        # 用例数
                        func.sum(func.if_(cls.step_type == 'api', func.if_(cls.status != "SKIP", 1, 0), 0)).label(
                            "count_case"),
                        # 成功用例数
                        func.sum(
                            func.if_(cls.step_type == 'api', func.if_(cls.status == "SUCCESS", 1, 0), 0)).label(
                            "count_case_success"),
                        # 失败用例数
                        func.sum(
                            func.if_(cls.step_type == 'api', func.if_(cls.status == "FAILURE", 1, 0), 0)).label(
                            "count_case_fail"),
                        # 测试用例通过率
                        func.round(
                            func.sum(
                                func.if_(cls.step_type == 'api',
                                         func.if_(cls.status == "SUCCESS", func.if_(cls.status != "SKIP", 1, 0), 0),
                                         0)) / func.sum(
                                func.if_(cls.step_type == 'api', func.if_(cls.status != "SKIP", 1, 0), 0)) * 100,
                            2).label("case_pass_rate"),
                        # 测试步骤通过率
                        func.round(
                            func.sum(func.if_(cls.status == "SUCCESS", 1, 0)) / func.count('1') * 100, 2).label(
                            "step_pass_rate")).where(*q)

                    return await cls.get_result(stmt, first=True)

            mode_class = ModelClass
            ApiTestReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls


class Env(Base):
    """环境表"""
    __tablename__ = 'env'

    name = Column(String(255), nullable=False, comment='环境名称', index=True)
    domain_name = Column(String(255), nullable=False, comment='url地址')
    remarks = Column(String(255), nullable=False, comment='说明')
    variables = Column(JSON(), nullable=False, comment='环境变量')
    headers = Column(JSON(), nullable=False, comment='环境请求头')
    data_sources = Column(JSON(), nullable=False, comment='数据源')

    @classmethod
    async def get_list(cls, params: EnvQuery = EnvQuery()):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        u = aliased(User)
        stmt = select(cls.id,
                      cls.name,
                      cls.domain_name,
                      cls.variables,
                      cls.headers,
                      cls.remarks,
                      cls.updated_by,
                      cls.created_by,
                      cls.creation_date,
                      cls.updation_date,
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'), ).where(*q) \
            .join(u, u.id == cls.updated_by) \
            .join(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取环境"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class EnvDataSource(Base):
    """环境数据源管理表"""
    __tablename__ = 'env_data_source'

    env_id = Column(Integer, nullable=True, index=True, comment='环境id')
    data_source_id = Column(Integer, nullable=True, index=True, comment='数据源id')

    @classmethod
    async def unbinding_data_source(cls, params: BindingDataSourceIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.data_source_id.in_(params.data_source_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.id,
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      DataSource.name,
                      DataSource.id.label("data_source_id"),
                      DataSource.host,
                      DataSource.port,
                      DataSource.type,
                      DataSource.user,
                      DataSource.updation_date,
                      DataSource.creation_date,
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(DataSource, DataSource.id == cls.data_source_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class EnvFunc(Base):
    """环境数据源管理表"""
    __tablename__ = 'env_func'

    env_id = Column(Integer, nullable=True, index=True, comment='环境id')
    func_id = Column(Integer, nullable=True, index=True, comment='辅助函数id')

    @classmethod
    async def unbinding_funcs(cls, params: BindingFuncIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.func_id.in_(params.func_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.get_table_columns(),
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      Functions.name.label("name"),
                      Functions.remarks.label("remarks"),
                      Functions.content.label("content"),
                      Functions.id.label("func_id"),
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(Functions, Functions.id == cls.func_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class Functions(Base):
    __tablename__ = 'functions'

    name = Column(Integer, nullable=False, comment='name')
    remarks = Column(Integer, nullable=False, comment='备注')
    project_id = Column(Integer, nullable=False, comment='关联项目')
    content = Column(Text, nullable=True, comment='自定义函数内容')
    func_type = Column(String(255), nullable=False, comment='函数类型')
    func_tags = Column(String(255), nullable=False, comment='函数标签')

    @classmethod
    async def get_list(cls, params: FuncQuery):
        q = [cls.enabled_flag == 1]
        if params.project_name:
            q.append(ProjectInfo.name.like(f'%{params.project_name}%'))
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        u = aliased(User)

        stmt = select(cls.get_table_columns(),
                      ProjectInfo.name.label('project_name'),
                      User.nickname.label('updated_by_name'),
                      u.nickname.label('created_by_name'), ).where(*q) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_by_id(cls, id: int):
        stmt = select(cls.get_table_columns(),
                      ProjectInfo.name.label('project_name')).where(cls.enabled_flag == 1, cls.id == id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id)

        return await cls.get_result(stmt, first=True)

    @classmethod
    def get_by_project_id(cls, project_id):
        return cls.query.filter(cls.project_id == project_id).first()


class DataSource(Base):
    """数据源"""
    __tablename__ = 'data_source'

    type = Column(String(255), nullable=False, comment='数据源类型', index=True)
    name = Column(String(255), nullable=False, comment='数据源名称', index=True)
    host = Column(String(255), nullable=False, comment='ip')
    port = Column(String(255), nullable=True, comment='端口')
    user = Column(String(255), nullable=False, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码')

    @classmethod
    async def get_list(cls, params: SourceQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.source_type:
            q.append(cls.type == params.source_type)
        if params.name:
            q.append(cls.name.like(f"%{params.name}%"))
        if params.source_ids and isinstance(params.source_ids, list):
            q.append(cls.id.in_(params.source_ids))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name'),
                      ).where(*q) \
            .outerjoin(User, cls.updated_by == User.id) \
            .outerjoin(u, cls.created_by == u.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter(cls.username == username, cls.enabled_flag == 1).first()
