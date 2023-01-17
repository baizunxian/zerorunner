from typing import List

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, func, \
    distinct, text, and_, JSON, DECIMAL, case as func_case
from sqlalchemy.orm import aliased

from autotest.models.Base import Base, TimestampMixin
from autotest.models.sys_models import User


class ProjectInfo(Base, TimestampMixin):
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
    def get_project_list(cls, id=None, name=None, created_by_name=None, ids=None):
        q = list()
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if created_by_name:
            q.append(User.nickname.like('%{}%'.format(created_by_name)))
        if id:
            q.append(cls.id == id)
        if ids:
            q.append(cls.id.in_(ids))
        u = aliased(User)
        return cls.query.outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .filter(*q, cls.enabled_flag == 1) \
            .with_entities(cls.id,
                           cls.name,
                           cls.responsible_name,
                           cls.config_id,
                           cls.test_user,
                           cls.dev_user,
                           cls.simple_desc,
                           cls.remarks,
                           cls.publish_app,
                           cls.updated_by,
                           cls.created_by,
                           cls.updation_date,
                           cls.creation_date,
                           u.nickname.label('updated_by_name'),
                           User.nickname.label('created_by_name')) \
            .order_by(cls.creation_date.desc())

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
    def get_project_by_name(cls, name):
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_project_ids(cls):
        return cls.query.filter(cls.enabled_flag == 1).with_entities(cls.id).all()

    @classmethod
    def get_project_by_product_id(cls, product_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.product_id == product_id).with_entities(cls.id).all()


class ModuleInfo(Base, TimestampMixin):
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
    def get_list(cls, name=None, project_name=None, project_id=None, order_field=None, sort_type=None,
                 user_ids=None, project_ids=None, ids=None):
        q = list()
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if project_id:
            q.append(cls.project_id == project_id)
        if project_name:
            q.append(ProjectInfo.project_name.like('%{}%'.format(project_name)))
        if user_ids:
            q.append(cls.created_by.in_(user_ids))
        if project_ids:
            q.append(cls.project_id.in_(project_ids))
        if ids:
            q.append(cls.id.in_(ids))
        # if packages_id:
        #     q.append(cls.packages_id == packages_id)
        if sort_type == 0:
            sort_type = 'asc'
        else:
            sort_type = 'desc'
        if not order_field or order_field == 'creation_date':
            order_field = 'module_info.creation_date'
        if order_field == 'project_name':
            order_field = 'project_info.name'
        if order_field == 'test_user':
            order_field = 'user.nickname'
        order_by = '{} {} {} {}'.format(order_field, sort_type, ',module_info.id', sort_type)
        u = aliased(User)
        return cls.query \
            .outerjoin(ProjectInfo, and_(cls.project_id == ProjectInfo.id, ProjectInfo.enabled_flag == 1)) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ApiInfo,
                       and_(cls.id == ApiInfo.module_id, ApiInfo.enabled_flag == 1)) \
            .with_entities(func.count(distinct(ApiInfo.id)).label('case_count'),
                           cls.id,
                           cls.name,
                           cls.project_id,
                           cls.config_id,
                           cls.test_user,
                           cls.simple_desc,
                           cls.remarks,
                           cls.leader_user,
                           cls.priority,
                           cls.module_packages,
                           cls.updated_by,
                           cls.created_by,
                           cls.updation_date,
                           cls.creation_date,
                           User.nickname.label('created_by_name'),
                           u.nickname.label('updated_by_name'),
                           ProjectInfo.name.label('project_name')) \
            .filter(*q, cls.enabled_flag == 1) \
            .group_by(cls.id) \
            .order_by(text(order_by))

    @classmethod
    def get_module_by_project_id(cls, project_id):
        """查询项目是否有关联模块"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1).all()

    @classmethod
    def get_module_by_name(cls, name):
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()

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


class ApiInfo(Base, TimestampMixin):
    """接口用例"""
    __tablename__ = 'api_info'

    name = Column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    module_id = Column(Integer, nullable=False, comment='所属模块')
    case_status = Column(Integer, nullable=True, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code_id = Column(BigInteger, nullable=True, comment='关联接口id')
    code = Column(String(255), nullable=True, comment='接口code')
    priority = Column(Integer, nullable=False, comment='优先级', default=3)
    case_tag = Column(String(255), nullable=True, comment='用例标签')
    method = Column(String(255), nullable=True, comment='请求方式')
    pre_steps = Column(JSON, nullable=True, comment='前置步骤')
    post_steps = Column(JSON, nullable=True, comment='后置步骤')
    setup_hooks = Column(JSON, nullable=True, comment='前置操作')
    teardown_hooks = Column(JSON, nullable=True, comment='后置操作')
    variables = Column(JSON, nullable=True, comment='变量')
    request_body = Column(JSON, nullable=True, comment='请求参数')
    headers = Column(JSON, nullable=True, comment='请求头')
    url = Column(JSON, nullable=True, comment='请求地址')
    validators = Column(JSON, nullable=True, comment='断言规则')
    extracts = Column(JSON, nullable=True, comment='提取')
    tags = Column(JSON, nullable=True, comment='用例标签')
    remarks = Column(String(255), nullable=True, comment='描述')

    @classmethod
    def get_list(cls, **kwargs):
        q = []
        id = kwargs.get("id", None)
        name = kwargs.get("name", None)
        project_id = kwargs.get("project_id", None)
        module_id = kwargs.get("module_id", None)
        code = kwargs.get("code", None)
        module_ids = kwargs.get("module_ids", None)
        project_ids = kwargs.get("project_ids", None)
        created_by = kwargs.get("created_by", None)
        created_by_name = kwargs.get("created_by_name", None)
        priority = kwargs.get("priority", None)
        ids = kwargs.get("ids", None)
        case_status = kwargs.get("case_status", None)
        sort_type = kwargs.get("sort_type", 1)
        order_field = kwargs.get("order_field", None)
        if id:
            q.append(cls.id == id)
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if project_id:
            q.append(cls.project_id == project_id)
        if module_id:
            q.append(cls.module_id == module_id)
        if code:
            q.append(cls.code.like('%{}%'.format(code)))
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        if project_ids:
            q.append(cls.project_id.in_(project_ids))
        if created_by:
            q.append(cls.created_by == created_by)
        if created_by_name:
            q.append(User.nickname.like('%{}%'.format(created_by_name)))
        if priority:
            q.append(cls.priority.in_(priority))
        if ids:
            q.append(cls.id.in_(ids))
        if case_status:
            q.append(cls.case_status == case_status)
        u = aliased(User)

        sort_type = 'asc' if sort_type == 0 else 'desc'

        if not order_field or order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        if order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        if order_field == 'name':
            order_field = 'api_info.name'
        if order_field == 'project_name':
            order_field = 'project_info.name'
        if order_field == 'module_name':
            order_field = 'module_info.name'
        if order_field == 'created_by_name' or order_field == 'updated_by_name':
            order_field = 'user.nickname'
        order_by = f'{order_field} {sort_type} {",api_info.id"} {sort_type}'

        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .with_entities(
            cls.id,
            cls.name,
            cls.url,
            cls.method,
            cls.project_id,
            cls.module_id,
            cls.code_id,
            cls.code,
            cls.priority,
            cls.case_status,
            cls.case_tag,
            cls.updated_by,
            cls.created_by,
            cls.updation_date,
            cls.creation_date,
            cls.enabled_flag,
            ProjectInfo.name.label('project_name'),
            ModuleInfo.name.label('module_name'),
            User.nickname.label('created_by_name'),
            u.nickname.label('updated_by_name')
        ) \
            .filter(*q, cls.enabled_flag == 1) \
            .order_by(text(order_by))

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.enabled_flag == 1, cls.type == 1).all()

    @classmethod
    def get_api_by_module_id(cls, module_id=None, module_ids=None):
        """查询模块是否有case关联"""
        q = list()
        if module_id:
            q.append(cls.module_id == module_id)
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        return cls.query.filter(*q, cls.enabled_flag == 1)

    @classmethod
    def get_api_by_project_id(cls, project_id):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1)

    @classmethod
    def get_api_by_name(cls, name):
        """获取用例名是否存在"""
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()

    @classmethod
    def get_api_by_ids(cls, ids: List):
        q = []
        return cls.query.filter(cls.id.in_(ids), *q, cls.enabled_flag == 1)

    @classmethod
    def get_api_by_id(cls, id: int):
        u = aliased(User)
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .with_entities(
            cls.id,
            cls.name,
            cls.url,
            cls.method,
            cls.project_id,
            cls.module_id,
            cls.code_id,
            cls.code,
            cls.priority,
            cls.case_status,
            cls.case_tag,
            cls.request_body,
            cls.pre_steps,
            cls.post_steps,
            cls.teardown_hooks,
            cls.setup_hooks,
            cls.extracts,
            cls.request_body,
            cls.headers,
            cls.validators,
            cls.remarks,
            cls.tags,
            cls.updated_by,
            cls.created_by,
            cls.updation_date,
            cls.creation_date,
            cls.enabled_flag,
            User.nickname.label('created_by_name'),
            u.nickname.label('updated_by_name')
        ).first()

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


class ApiCase(Base, TimestampMixin):
    """测试套件，集合"""
    __tablename__ = 'api_case'

    name = Column(String(64), nullable=False, comment='名称', index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    remarks = Column(String(255), nullable=False, comment='备注')
    env_id = Column(Integer, nullable=False, comment='环境id')
    headers = Column(JSON, nullable=False, comment='场景请求头')
    variables = Column(JSON, nullable=False, comment='场景变量')
    step_data = Column(JSON, nullable=False, comment='场景步骤')

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

    @classmethod
    def get_case_by_id(cls, id):
        """根据套件id查询套件"""
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    def get_case_by_name(cls, suite_name):
        """根据套件名称查询套件"""
        return cls.query.filter(cls.suite_name == suite_name, cls.enabled_flag == 1).all()

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


class ApiCaseStep(Base, TimestampMixin):
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


class ApiTestReport(Base, TimestampMixin):
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
    def get_list(cls, id=None, name=None, project_id=None, module_id=None, run_user_name=None, min_and_max=None,
                 user_ids=None, project_ids=None, ids=None, status=None, execute_source=None, created_by=None,
                 execute_user_name=None):
        q = []
        if id:
            q.append(cls.id == id)
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if project_id:
            q.append(cls.project_id == project_id)
        if module_id:
            q.append(cls.module_id == module_id)
        if status:
            q.append(cls.status == status)
        if execute_source:
            q.append(cls.execute_source == execute_source)
        if run_user_name:
            q.append(User.created_by.like('%{}%'.format(run_user_name)))
        if ids:
            q.append(cls.id.in_(ids))
        if user_ids:
            q.append(cls.execute_user_id.in_(user_ids))
        if created_by:
            q.append(cls.created_by == created_by)
        if project_ids:
            q.append(cls.project_id.in_(project_ids))
        if min_and_max:
            q.append(cls.creation_date.between(*min_and_max))
        if execute_user_name:
            q.append(User.nickname.like('%{}%'.format(execute_user_name)))

        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(cls.id,
                           cls.name,
                           cls.start_time,
                           cls.duration,
                           cls.case_id,
                           cls.run_mode,
                           cls.run_type,
                           cls.success,
                           cls.run_count,
                           cls.actual_run_count,
                           cls.run_success_count,
                           cls.run_log,
                           cls.project_id,
                           cls.module_id,
                           cls.creation_date,
                           User.nickname.label('run_user_name')) \
            .order_by(cls.creation_date.desc())

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
            class ModelClass(Base, TimestampMixin):
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
                session_data = Column(JSON, nullable=True, comment='请求会话数据')
                export_vars = Column(JSON, nullable=True, comment='导出变量')
                report_id = Column(Integer, nullable=True, comment='报告id', index=True)
                start_time = Column(DateTime, nullable=True, comment='开始时间')
                duration = Column(DECIMAL(), nullable=True, comment='耗时')
                pre_hook_data = Column(JSON, nullable=True, comment='前置步骤')
                post_hook_data = Column(JSON, nullable=True, comment='后置步骤')
                index = Column(Integer, nullable=True, comment='顺序')
                status_code = Column(Integer, nullable=True, comment='顺序')
                response_time_ms = Column(DECIMAL(), nullable=True, comment='响应耗时')
                elapsed_ms = Column(DECIMAL(), nullable=True, comment='请求耗时')

                @classmethod
                def get_list(cls, report_id, parent_step_id=None):
                    q = list()
                    q.append(cls.report_id == report_id)
                    if parent_step_id:
                        q.append(cls.parent_step_id == parent_step_id)
                    else:
                        q.append(cls.parent_step_id == None)

                    return cls.query.filter(*q, cls.enabled_flag == 1) \
                        .outerjoin(ApiInfo, ApiInfo.id == cls.case_id) \
                        .outerjoin(User, User.id == ApiInfo.created_by) \
                        .with_entities(cls.id,
                                       cls.name,
                                       cls.case_id,
                                       cls.success,
                                       cls.status,
                                       cls.step_id,
                                       cls.parent_step_id,
                                       cls.step_type,
                                       cls.message,
                                       cls.variables,
                                       cls.session_data,
                                       cls.export_vars,
                                       cls.step_tag,
                                       cls.report_id,
                                       cls.pre_hook_data,
                                       cls.post_hook_data,
                                       cls.response_time_ms,
                                       cls.status_code,
                                       cls.elapsed_ms,
                                       ApiInfo.name.label("case_name"),
                                       ApiInfo.method.label("method"),
                                       ApiInfo.url.label("url"),
                                       ApiInfo.created_by.label('case_created_by'),
                                       User.nickname.label('case_created_by_name'),
                                       ) \
                        .order_by(cls.index)

                @classmethod
                def statistics(cls, report_id, parent_step_id=None):
                    q = list()
                    q.append(cls.report_id == report_id)
                    if parent_step_id:
                        q.append(cls.parent_step_id == parent_step_id)
                    else:
                        q.append(cls.parent_step_id == None)

                    return cls.query.filter(*q, cls.enabled_flag == 1) \
                        .with_entities(
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
                        func.sum(func.if_(cls.step_type == 'case', func.if_(cls.status != "SKIP", 1, 0), 0)).label(
                            "count_case"),
                        # 成功用例数
                        func.sum(
                            func.if_(cls.step_type == 'case', func.if_(cls.status == "SUCCESS", 1, 0), 0)).label(
                            "count_case_success"),
                        # 失败用例数
                        func.sum(
                            func.if_(cls.step_type == 'case', func.if_(cls.status == "FAILURE", 1, 0), 0)).label(
                            "count_case_fail"),
                        # 测试用例通过率
                        func.round(
                            func.sum(
                                func.if_(cls.step_type == 'case',
                                         func.if_(cls.status == "SUCCESS", func.if_(cls.status != "SKIP", 1, 0), 0),
                                         0)) / func.sum(
                                func.if_(cls.step_type == 'case', func.if_(cls.status != "SKIP", 1, 0), 0)) * 100,
                            2).label("case_pass_rate"),
                        # 测试步骤通过率
                        func.round(
                            func.sum(func.if_(cls.status == "SUCCESS", 1, 0)) / func.count('1') * 100, 2).label(
                            "step_pass_rate"),
                    ).first()

            mode_class = ModelClass
            ApiTestReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls


class Env(Base, TimestampMixin):
    """环境表"""
    __tablename__ = 'env'

    name = Column(String(255), nullable=False, comment='环境名称', index=True)
    domain_name = Column(String(255), nullable=False, comment='url地址')
    remarks = Column(String(255), nullable=False, comment='说明')
    variables = Column(JSON(), nullable=False, comment='环境变量')
    headers = Column(JSON(), nullable=False, comment='环境请求头')
    data_sources = Column(JSON(), nullable=False, comment='数据源')

    @classmethod
    def get_list(cls, name=None, created_by_name=None):
        q = []
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if created_by_name:
            q.append(User.nickname.like('%{}%'.format(created_by_name)))
        u = aliased(User)
        return cls.query.outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .filter(*q, cls.enabled_flag == 1) \
            .with_entities(cls.id,
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
                           u.nickname.label('updated_by_name'),
                           ) \
            .order_by(cls.creation_date.desc())

    @classmethod
    def get_env_by_name(cls, name):
        """根据环境名称获取环境"""
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()


class TimedTask(Base, TimestampMixin):
    """定时任务表"""
    __tablename__ = 'celery_periodic_task'

    name = Column(String(255), nullable=True, comment='定时任务名', index=True)
    task = Column(String(255), comment='任务路径')
    args = Column(String(255), comment='参数')
    kwargs = Column(String(255), comment='关键字参数')
    queue = Column(String(255), comment='队列')
    exchange = Column(String(255), comment='交换')
    routing_key = Column(String(255), comment='路由密钥')
    expires = Column(DateTime, comment='到期时间')
    enabled = Column(String(255), comment='是否启用, 1启动，0停用', default=0)
    last_run_at = Column(String(255), comment='上次运行时间')
    total_run_count = Column(String(255), comment='运行总次数', default=0)
    date_changed = Column(DateTime, comment='更改日期')
    description = Column(String(255), comment='备注')
    crontab_id = Column(Integer, comment='定时器id')
    interval_id = Column(Integer, comment='参数')
    run_mode = Column(String(255), nullable=False, comment='作业类型, case, module, suite')
    run_type = Column(Integer, nullable=False, comment='30 定时任务')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    suite_id = Column(Integer, nullable=True, comment='套件id')
    case_ids = Column(String(255), nullable=False, comment='用例集合')

    @classmethod
    def get_list(cls, id=None, name=None, user_ids=None, created_by_name=None, created_by=None, project_ids=None):
        q = list()
        u = aliased(User)
        if id:
            q.append(cls.id == id)
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if created_by_name:
            q.append(u.nickname.like('%{}%'.format(created_by_name)))
        if user_ids:
            q.append(cls.created_by.in_(user_ids))
        if created_by:
            q.append(cls.created_by == created_by)
        if project_ids:
            q.append(cls.project_id.in_(project_ids))
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .with_entities(cls,
                           cls.id,
                           cls.name,
                           cls.task,
                           cls.args,
                           cls.kwargs,
                           cls.queue,
                           cls.exchange,
                           cls.routing_key,
                           cls.expires,
                           cls.enabled,
                           cls.last_run_at,
                           cls.total_run_count,
                           cls.date_changed,
                           cls.description,
                           cls.crontab_id,
                           cls.interval_id,
                           cls.run_type,
                           cls.project_id,
                           cls.module_id,
                           cls.suite_id,
                           cls.case_ids,
                           cls.updated_by,
                           cls.created_by,
                           cls.updation_date,
                           cls.creation_date,
                           u.nickname.label('created_by_name'),
                           User.nickname.label('updated_by_name'),
                           ProjectInfo.name.label('project_name'),
                           ModuleInfo.name.label('module_name')) \
            .order_by(cls.creation_date.desc())

    @classmethod
    def get_task_by_name(cls, name):
        """获取任务名存在的个数"""
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()


class Crontab(Base, TimestampMixin):
    """crontab 表"""
    __tablename__ = 'celery_crontab_schedule'

    minute = Column(String(255), comment='分钟')
    hour = Column(String(255), comment='小时')
    day_of_week = Column(String(255), comment='日期')
    day_of_month = Column(String(255), comment='月份')
    month_of_year = Column(String(255), comment='年')
    timezone = Column(String(255), comment='时区', default='Asia/Shanghai')

    @classmethod
    def get_crontab_by_parameter(cls, minute, hour, day_of_week, day_of_month, month_of_year):
        return cls.query.filter(cls.minute == minute, cls.hour == hour, cls.day_of_week == day_of_week,
                                cls.day_of_month == day_of_month, cls.month_of_year == month_of_year).first()


class PeriodicTaskChanged(Base):
    """定时任务更新表"""
    __tablename__ = 'celery_periodic_task_changed'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    last_update = Column(DateTime, comment='到期时间')

    @classmethod
    def get_data(cls):
        return cls.query.first()


class Functions(Base, TimestampMixin):
    __tablename__ = 'functions'

    name = Column(Integer, nullable=False, comment='name')
    remarks = Column(Integer, nullable=False, comment='备注')
    project_id = Column(Integer, nullable=False, comment='关联项目')
    content = Column(Text, nullable=True, comment='自定义函数内容')

    @classmethod
    def get_list(cls, project_name=None, name=None):
        q = []
        if project_name:
            q.append(ProjectInfo.name.like(f'%{project_name}%'))
        if name:
            q.append(cls.name.like(f'%{name}%'))
        u = aliased(User)
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .outerjoin(u, u.id == cls.created_by) \
            .with_entities(cls.id,
                           cls.project_id,
                           cls.name,
                           cls.remarks,
                           cls.content,
                           cls.creation_date,
                           cls.updation_date,
                           ProjectInfo.name.label('project_name'),
                           User.nickname.label('updated_by_name'),
                           u.nickname.label('created_by_name'),
                           ) \
            .order_by(cls.creation_date.desc())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.enabled_flag == 1, cls.id == id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .with_entities(cls.id,
                           cls.project_id,
                           cls.content,
                           cls.name,
                           cls.remarks,
                           cls.creation_date,
                           cls.updation_date,
                           ProjectInfo.name.label('project_name')) \
            .first()

    @classmethod
    def get_by_project_id(cls, project_id):
        return cls.query.filter(cls.project_id == project_id).first()
