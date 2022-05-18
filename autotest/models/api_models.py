from typing import List

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, BigInteger, func, \
    distinct, text, and_
from sqlalchemy.orm import aliased

from autotest.models.Base import Base, TimestampMixin
from autotest.models.sys_models import User


class ProjectInfo(Base, TimestampMixin):
    """项目表"""
    __tablename__ = 'project_info'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

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
    def get_project_list(cls, name=None, created_by_name=None, ids=None):
        q = list()
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if created_by_name:
            q.append(User.nickname.like('%{}%'.format(created_by_name)))
        if ids:
            q.append(cls.id.in_(ids))
        u = aliased(User)
        return cls.query.outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .filter(*q, cls.enabled_flag == 1) \
            .with_entities(cls,
                           cls.id,
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
            .outerjoin(CaseInfo,
                       and_(cls.id == CaseInfo.module_id, CaseInfo.enabled_flag == 1, CaseInfo.case_type == 1)) \
            .with_entities(func.count(distinct(CaseInfo.id)).label('case_count'),
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


class CaseInfo(Base, TimestampMixin):
    """测试用例，测试配置"""
    __tablename__ = 'case_info'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    case_type = Column(Integer, nullable=False, comment='test/config,测试类型, 1 case  2 config', default=1)
    name = Column(String(255), nullable=False, comment='用例/配置名称', index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    module_id = Column(Integer, nullable=False, comment='所属模块')
    include = Column(Text, nullable=True, comment='前置config/test')
    testcase = Column(Text, nullable=True, comment='用例信息')
    service_name = Column(String(1024), nullable=True, comment='所属服务名称')
    # run_type = Column(Integer, nullable=True, comment='运行方式(0:集成运行,1:独立运行)', default=1)
    code_id = Column(BigInteger, nullable=True, comment='关联接口id')
    code = Column(String(255), nullable=True, comment='接口code')
    config_id = Column(Integer, nullable=True, comment='用例配置id')
    priority = Column(Integer, nullable=False, comment='优先级', default=3)
    case_status = Column(Integer, nullable=True, comment='用例状态 10, 生效 ， 20 失效', default=10)
    case_tab = Column(Integer, nullable=True, comment='用例标签')

    @classmethod
    def get_list(cls, id=None, name=None, project_id=None, module_id=None, created_by_name=None, case_type=1,
                 module_ids=None, code=None, created_by=None, priority=None, sort_type=1, order_field=None, ids=None,
                 project_ids=None, case_status=None):
        q = list()
        if id:
            q.append(cls.id == id)
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        if project_id:
            q.append(cls.project_id == project_id)
        if module_id:
            q.append(cls.module_id == module_id)
        if case_type:
            q.append(cls.case_type == case_type)
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
            order_field = 'case_info.creation_date'
        if order_field == 'updation_date':
            order_field = 'case_info.updation_date'
        if order_field == 'name':
            order_field = 'case_info.name'
        if order_field == 'project_name':
            order_field = 'project_info.name'
        if order_field == 'module_name':
            order_field = 'module_info.name'
        if order_field == 'created_by_name' or order_field == 'updated_by_name':
            order_field = 'user.nickname'
        order_by = f'{order_field} {sort_type} {",case_info.id"} {sort_type}'

        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .with_entities(
            cls.id,
            cls.name,
            cls.case_type,
            cls.service_name,
            cls.project_id,
            cls.module_id,
            cls.include,
            # cls.run_type,
            cls.code_id,
            cls.code,
            cls.config_id,
            cls.priority,
            cls.case_status,
            cls.case_tab,
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
    def get_case_by_module_id(cls, module_id=None, module_ids=None, case_type=None):
        """查询模块是否有case关联"""
        q = list()
        if case_type:
            q.append(cls.case_type == case_type)
        if module_id:
            q.append(cls.module_id == module_id)
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        return cls.query.filter(*q, cls.enabled_flag == 1)

    @classmethod
    def get_case_by_project_id(cls, project_id):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1)

    @classmethod
    def get_case_by_name(cls, name, case_type=1):
        """获取用例名是否存在"""
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1, cls.case_type == case_type).first()

    @classmethod
    def get_case_by_ids(cls, ids: List, case_type: int = 1):
        q = []
        if case_type:
            q.append(cls.case_type == case_type)
        return cls.query.filter(cls.id.in_(ids), *q, cls.enabled_flag == 1)

    @classmethod
    def get_case_by_time(cls, start_time, end_time):
        return cls.query.filter(cls.creation_date.between(start_time, end_time), cls.enabled_flag == 1)

    @classmethod
    def statistic_project_case_number(cls):
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectInfo.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1, cls.case_type == 1)

    @classmethod
    def get_case_by_project_id_or_body(cls, project_id, body_name):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.request.like(('%{}%'.format(body_name))),
                                cls.enabled_flag == 1) \
            .with_entities(cls.id) \
            .all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()


class TestSuite(Base, TimestampMixin):
    """测试套件，集合"""
    __tablename__ = 'test_suite'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(64), nullable=False, comment='名称', index=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    include = Column(String(1024), nullable=True, comment='用例列表')
    config_id = Column(Integer, nullable=False, comment='配置ID')
    remarks = Column(String(255), nullable=False, comment='备注')

    @classmethod
    def get_list(cls, name=None, user_ids=None, project_id=None, created_by=None, suite_type=None,
                 created_by_name=None, project_ids=None, ids=None):
        q = list()
        if name:
            q.append(cls.suite_name.like(f'%{name}%'))
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
                           cls.include,
                           cls.config_id,
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
    def get_suite_by_id(cls, id):
        """根据套件id查询套件"""
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    def get_suite_by_name(cls, suite_name):
        """根据套件名称查询套件"""
        return cls.query.filter(cls.suite_name == suite_name, cls.enabled_flag == 1).all()

    @classmethod
    def statistic_project_suite_number(cls):
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


class TestReports(Base, TimestampMixin):
    """报告表"""
    __tablename__ = 'test_reports'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(64), nullable=False, comment='报告名', index=True)
    start_at = Column(String(64), nullable=True, comment='开始时间')
    scene_num = Column(Integer, nullable=True, comment='用例数量')
    duration = Column(String(255), nullable=True, comment='用例执行时长')
    run_type = Column(String(100), nullable=True, comment='运行类型 手动, 定时任务, 异步', default=10)
    run_mode = Column(String(100), nullable=True, comment='运行模式，1同步，2异步，3定时任务')
    task_type = Column(String(100), nullable=True, comment='任务类型, test,module,project')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    report_type = Column(Integer, nullable=True, comment='报告类型，10测试报告，20数据构造, 30调试报告')
    run_case_priority = Column(Integer, nullable=True, comment='执行用例等级')
    execute_service = Column(String(100), nullable=True, comment='执行服务')
    execute_source = Column(Integer, nullable=True, comment='执行来源')
    execute_user_id = Column(Integer, nullable=False, comment='执行人id')
    successful_use_case = Column(Integer, nullable=True, comment='成功用例')
    success = Column(String(100), nullable=True, comment='成功状态')
    run_test_count = Column(Integer, nullable=True, comment='运行用例个数')
    report_body = Column(Text, nullable=True, comment='报告详情')

    @classmethod
    def get_list(cls, id=None, name=None, project_id=None, module_id=None, execute_user_name=None, min_and_max=None,
                 user_ids=None, project_ids=None, ids=None, status=None, execute_source=None, created_by=None):
        q = list()
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
        if execute_user_name:
            q.append(User.nickname.like('%{}%'.format(execute_user_name)))
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

        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.execute_user_id) \
            .with_entities(cls.id,
                           cls.name,
                           cls.start_at,
                           cls.scene_num,
                           cls.duration,
                           cls.run_type,
                           cls.run_mode,
                           cls.task_type,
                           cls.project_id,
                           cls.module_id,
                           cls.report_type,
                           cls.run_case_priority,
                           cls.execute_service,
                           cls.execute_source,
                           cls.execute_user_id,
                           cls.successful_use_case,
                           cls.success,
                           cls.run_test_count,
                           # cls.report_body, // 报告内容太大，列表不返回
                           User.nickname.label('execute_user_name')) \
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
                           cls.start_at,
                           cls.success,
                           cls.run_test_count,
                           cls.successful_use_case,
                           cls.execute_user_id,
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


class TestReportsNew(object):
    """报告表"""
    _mapper = {}

    @staticmethod
    def model(id):
        table_index = id % 100
        class_name = 'TestReportsNew_%d' % table_index

        ModelClass = TestReportsNew._mapper.get(class_name, None)
        if ModelClass is None:
            class ModelClass(Base, TimestampMixin):
                __module__ = __name__
                __name__ = class_name,
                __tablename__ = 'test_reports_new_%d' % table_index
                id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
                # summary
                summary_report_name = Column(String(64), nullable=False, comment='报告名称', index=True)
                summary_success = Column(String(64), nullable=False, comment='结果是否成功')
                summary_start_at = Column(Float, nullable=False, comment='开始时间戳')
                summary_duration = Column(Float, nullable=False, comment='耗时（秒）')

                # detail
                detail_base_url = Column(String(64), nullable=True, comment='')
                detail_output = Column(String(64), nullable=True, comment='')

                # records
                records_attachment = Column(String(64), nullable=True, comment='')

                # request
                request_url = Column(String(256), nullable=True, comment='url')
                request_method = Column(String(64), nullable=True, comment='method')
                request_headers = Column(String(512), nullable=True, comment='headers')
                request_start_timestamp = Column(String(64), nullable=True, comment='start_timestamp')
                request_body = Column(String(1024), nullable=True, comment='body')

                # response
                response_status_code = Column(Integer, nullable=True, comment='http状态码')
                response_headers = Column(String(512), nullable=True, comment='headers')
                response_content_size = Column(Integer, nullable=True, comment='')
                response_time_ms = Column(Float, nullable=True, comment='')
                response_elapsed_ms = Column(Float, nullable=True, comment='')
                response_encoding = Column(String(64), nullable=True, comment='')
                response_content = Column(String(2048), nullable=True, comment='')
                response_content_type = Column(String(64), nullable=True, comment='')

                # validators
                validators_check = Column(String(64), nullable=True, comment='')
                validators_expect = Column(String(64), nullable=True, comment='')
                validators_comparator = Column(String(64), nullable=True, comment='')
                validators_check_value = Column(String(64), nullable=True, comment='')
                validators_check_result = Column(String(64), nullable=True, comment='')

                # output
                output_out = Column(String(2048), nullable=True, comment='输出参数')

                # basic
                c_id = Column(Integer, nullable=True, comment='用例id')
                basic_execute_user = Column(String(64), nullable=True, comment='执行人')
                basic_execute_user_id = Column(Integer, nullable=True, comment='执行人id')
                basic_project = Column(String(64), nullable=True, comment='项目')
                basic_project_id = Column(Integer, nullable=True, comment='项目id')
                basic_module = Column(String(64), nullable=True, comment='模块')
                basic_module_id = Column(Integer, nullable=True, comment='模块id')
                basic_type = Column(String(64), nullable=False, comment='任务类型 case,suite,module,project',
                                    default='case')
                basic_run_type = Column(Integer, nullable=False, comment='运行类型 手动10,异步20,CICD30', default=10)
                basic_batch = Column(Integer, nullable=False, comment='批次id')
                basic_extend_integer_1 = Column(Integer, nullable=True, comment='扩展_integer_1')
                basic_extend_string_1 = Column(String(64), nullable=True, comment='扩展_string_1')
                basic_extend_float_1 = Column(String(64), nullable=True, comment='扩展_float_1')

                @classmethod
                def get_list(cls, id=None, summary_report_name=None, basic_project_id=None, basic_module_id=None,
                             basic_execute_user=None, response_status_code=None, request_method=None,
                             basic_batch=None, summary_success=None, ids=None, basic_execute_user_id=None,
                             case_created_by_name=None, project_ids=None, c_id=None):
                    q = list()
                    if id:
                        q.append(cls.id == id)
                    if summary_report_name:
                        q.append(cls.summary_report_name.like('%{}%'.format(summary_report_name)))
                    if c_id:
                        q.append(cls.c_id == c_id)
                    if basic_project_id:
                        q.append(cls.basic_project_id == basic_project_id)
                    if basic_module_id:
                        q.append(cls.basic_module_id == basic_module_id)
                    if basic_batch:
                        q.append(cls.basic_batch == basic_batch)
                    if summary_success != None:
                        q.append(cls.summary_success == summary_success)
                    if response_status_code:
                        q.append(cls.response_status_code == response_status_code)
                    if request_method:
                        q.append(cls.request_method == request_method)
                    if ids:
                        q.append(cls.id.in_(ids))
                    if basic_execute_user:
                        q.append(User.nickname.like('%{}%'.format(basic_execute_user)))
                    if basic_execute_user_id:
                        q.append(cls.basic_execute_user_id == basic_execute_user_id)
                    if case_created_by_name:
                        q.append(User.nickname.like('%{}%'.format(case_created_by_name)))
                    if project_ids:
                        q.append(cls.project_id.in_(project_ids))
                    return cls.query.filter(*q, cls.enabled_flag == 1) \
                        .outerjoin(CaseInfo, CaseInfo.id == cls.c_id) \
                        .outerjoin(User, User.id == CaseInfo.created_by) \
                        .with_entities(cls.id,
                                       cls.summary_report_name,
                                       cls.request_start_timestamp,
                                       cls.summary_success,
                                       cls.summary_duration,
                                       cls.request_method,
                                       cls.response_status_code,
                                       cls.basic_project,
                                       cls.basic_module,
                                       cls.basic_batch,
                                       cls.c_id,
                                       cls.basic_execute_user,
                                       CaseInfo.created_by.label('case_created_by'),
                                       User.nickname.label('case_created_by_name'),
                                       ) \
                        .order_by(cls.creation_date.desc())

                @classmethod
                def get_by_batch(cls, batch):
                    return cls.query.filter(cls.basic_batch == batch, cls.enabled_flag == 1)

                @classmethod
                def get_by_batch_new(cls, batch):
                    return cls.query.filter(cls.basic_batch == batch, cls.enabled_flag == 1).all()

                @classmethod
                def rdp_get_by_batch(cls, batch):
                    return cls.query.filter(cls.basic_batch == batch, cls.enabled_flag == 1) \
                        .with_entities(cls.summary_success, cls.summary_duration).all()

                @classmethod
                def get_output_by_batch(cls, batch):
                    return cls.query.filter(cls.basic_batch == batch, cls.enabled_flag == 1) \
                        .with_entities(cls.output_out) \
                        .order_by(cls.id.desc()).first()

            TestReportsNew._mapper[class_name] = ModelClass

        cls = ModelClass()
        cls.id = id
        return cls


class Env(Base, TimestampMixin):
    """环境表"""
    __tablename__ = 'env'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False, comment='环境名称', index=True)
    url = Column(String(255), nullable=False, comment='url地址')
    remarks = Column(String(255), nullable=False, comment='说明')

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
                           cls.url,
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

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
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
    run_type = Column(Integer, nullable=False, comment='作业类型, case, module, suite')
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

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
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


class DebugTalk(Base, TimestampMixin):
    __tablename__ = 'debug_talk'

    id = Column(BigInteger, primary_key=True, info='主键')
    project_id = Column(Integer, nullable=False, comment='项目id')
    debug_talk = Column(Text, nullable=True, comment='自定义函数内容')

    @classmethod
    def get_list(cls, project_name=None):
        q = []
        if project_name:
            q.append(ProjectInfo.name.like(f'%{project_name}%'))
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .with_entities(cls.id,
                           cls.project_id,
                           cls.debug_talk,
                           cls.creation_date,
                           cls.updation_date,
                           ProjectInfo.name.label('project_name'),
                           User.nickname.label('updated_by_name')
                           ) \
            .order_by(cls.creation_date.desc())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.enabled_flag == 1, cls.id == id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .with_entities(cls.id,
                           cls.project_id,
                           cls.debug_talk,
                           cls.creation_date,
                           cls.updation_date,
                           ProjectInfo.name.label('project_name')) \
            .first()

    @classmethod
    def get_by_project_id(cls, project_id):
        return cls.query.filter(cls.project_id == project_id).first()
