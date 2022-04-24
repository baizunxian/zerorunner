from sqlalchemy import Column, String, Integer, Text
from .Base import Base, TimestampMixin
from .sys_models import User


class Page(Base, TimestampMixin):
    """页面表"""
    __tablename__ = 'ui_page'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    page_name = Column(String(255), nullable=False, comment='页面名称', index=True)
    page_url = Column(String(255), nullable=False, comment='页面ui', index=True)
    project_id = Column(String(255), nullable=True, comment='项目id', index=True)
    module_id = Column(String(255), nullable=True, comment='模块id', index=True)
    remark = Column(String(255), nullable=True, comment='备注', index=True)

    @classmethod
    def get_list(cls, page_name=None):
        q = []
        if page_name:
            q.append(cls.page_name.like('%{}%'.format(page_name)))
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.creation_date.desc())

    @classmethod
    def get_page_by_url(cls, page_url):
        return cls.query.filter(cls.page_name == page_url, cls.enabled_flag == 1).first()


class Element(Base, TimestampMixin):
    """元素表"""
    __tablename__ = 'ui_element'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    element_name = Column(String(255), nullable=False, comment='元素名称', index=True)
    by_type = Column(String(255), nullable=True, comment='定位类型')
    by_value = Column(String(255), nullable=True, comment='定位元素值')
    page_id = Column(Integer, nullable=False, comment='定位元素值')
    remark = Column(String(255), nullable=True, comment='备注')

    @classmethod
    def get_list(cls, page_id, element_name=None):
        q = []
        if page_id:
            q.append(cls.page_id == page_id)
        if element_name:
            q.append(cls.element_name.like('%{}%'.format(element_name)))
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.creation_date.desc())

    @classmethod
    def get_el_by_page_id(cls, page_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.page_id == page_id)

    @classmethod
    def get_el_by_page_id_list(cls, page_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.page_id == page_id) \
            .with_entities(cls.element_name.label('name'),
                           cls.by_type,
                           cls.by_value,
                           cls.element_name,
                           cls.id).all()


class UiCase(Base, TimestampMixin):
    """ui 用例表"""
    __tablename__ = 'ui_case'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False, comment='用例名', index=True)
    condition = Column(String(255), nullable=True, comment='前置条件')
    flag = Column(Integer, nullable=True, comment='自动化标记')
    result = Column(String(255), nullable=True, comment='运行结果')
    steps = Column(Text, nullable=True, comment='运行步骤')
    remark = Column(String(255), nullable=True, comment='备注')

    @classmethod
    def get_list(cls, name=None):
        q = []
        if name:
            q.append(cls.name.like('%{}%'.format(name)))
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(cls.id,
                           cls.name,
                           cls.condition,
                           cls.created_by,
                           cls.flag,
                           cls.result,
                           cls.steps,
                           cls.remark,
                           cls.creation_date,
                           cls.updation_date,
                           User.nickname.label('created_by_name'))\
            .order_by(cls.creation_date.desc())


class Steps(Base, TimestampMixin):
    """步骤表"""
    __tablename__ = 'ui_steps'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    no = Column(Integer, nullable=False, comment='步骤排序', index=True)
    operate = Column(String(255), nullable=True, comment='操作')
    data = Column(String(255), nullable=True, comment='输入数据')
    by = Column(String(255), nullable=True, comment='定位元素方式')
    value = Column(String(255), nullable=True, comment='定位元素值')
    output = Column(String(255), nullable=True, comment='输出')
    remark = Column(String(255), nullable=True, comment='备注')
    ui_case_id = Column(Integer, nullable=True, comment='关联ui测试用例')


class UiReports(Base, TimestampMixin):
    """报告表"""
    __tablename__ = 'ui_reports'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    report_name = Column(String(255), nullable=False, comment='报告名', index=True)
    result = Column(Text, nullable=False, comment='报告结果', index=True)
    project_id = Column(String(255), nullable=True, comment='项目id', index=True)
    module_id = Column(String(255), nullable=True, comment='模块id', index=True)
    summary_success = Column(Integer(), nullable=True, comment='是否成功', index=True)
    summary_start_at = Column(String(255), nullable=True, comment='开始时间', index=True)
    summary_duration = Column(String(255), nullable=True, comment='执行时间', index=True)
    c_id = Column(Integer(), nullable=True, comment='用例id', index=True)
    remark = Column(String(255), nullable=True, comment='备注', index=True)

    @classmethod
    def get_list(cls, report_name=None):
        q = []
        if report_name:
            q.append(cls.report_name.like('%{}%'.format(report_name)))
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.creation_date.desc())
