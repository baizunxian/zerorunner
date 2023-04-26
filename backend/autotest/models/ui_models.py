from sqlalchemy import Column, String, Integer, Text

from autotest.models.base import Base


class Page(Base):
    """页面表"""
    __tablename__ = 'ui_page'

    page_name = Column(String(255), nullable=False, comment='页面名称', index=True)
    page_url = Column(String(255), nullable=False, comment='页面ui', index=True)
    project_id = Column(String(255), nullable=True, comment='项目id', index=True)
    module_id = Column(String(255), nullable=True, comment='模块id', index=True)
    remark = Column(String(255), nullable=True, comment='备注', index=True)


class Element(Base):
    """元素表"""
    __tablename__ = 'ui_element'

    element_name = Column(String(255), nullable=False, comment='元素名称', index=True)
    by_type = Column(String(255), nullable=True, comment='定位类型')
    by_value = Column(String(255), nullable=True, comment='定位元素值')
    page_id = Column(Integer, nullable=False, comment='定位元素值')
    remark = Column(String(255), nullable=True, comment='备注')


class UiCase(Base):
    """ui 用例表"""
    __tablename__ = 'ui_case'

    name = Column(String(255), nullable=False, comment='用例名', index=True)
    condition = Column(String(255), nullable=True, comment='前置条件')
    flag = Column(Integer, nullable=True, comment='自动化标记')
    result = Column(String(255), nullable=True, comment='运行结果')
    steps = Column(Text, nullable=True, comment='运行步骤')
    remark = Column(String(255), nullable=True, comment='备注')


class Steps(Base):
    """步骤表"""
    __tablename__ = 'ui_steps'

    no = Column(Integer, nullable=False, comment='步骤排序', index=True)
    operate = Column(String(255), nullable=True, comment='操作')
    data = Column(String(255), nullable=True, comment='输入数据')
    by = Column(String(255), nullable=True, comment='定位元素方式')
    value = Column(String(255), nullable=True, comment='定位元素值')
    output = Column(String(255), nullable=True, comment='输出')
    remark = Column(String(255), nullable=True, comment='备注')
    ui_case_id = Column(Integer, nullable=True, comment='关联ui测试用例')


class UiReports(Base):
    """报告表"""
    __tablename__ = 'ui_reports'

    report_name = Column(String(255), nullable=False, comment='报告名', index=True)
    result = Column(Text, nullable=False, comment='报告结果', index=True)
    project_id = Column(String(255), nullable=True, comment='项目id', index=True)
    module_id = Column(String(255), nullable=True, comment='模块id', index=True)
    summary_success = Column(Integer(), nullable=True, comment='是否成功', index=True)
    summary_start_at = Column(String(255), nullable=True, comment='开始时间', index=True)
    summary_duration = Column(String(255), nullable=True, comment='执行时间', index=True)
    c_id = Column(Integer(), nullable=True, comment='用例id', index=True)
    remark = Column(String(255), nullable=True, comment='备注', index=True)
