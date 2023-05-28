from sqlalchemy import Column, String, Integer, JSON, select
from sqlalchemy.orm import aliased

from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.ui.ui_case import UiCaseQuery
from autotest.schemas.ui.ui_element import UiElementQuery
from autotest.schemas.ui.ui_page import UiPageQuery


class UiPage(Base):
    """页面表"""
    __tablename__ = 'ui_page'

    name = Column(String(255), nullable=False, comment='页面名称', index=True)
    url = Column(String(255), nullable=False, comment='url')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    tags = Column(JSON, nullable=False, comment='标签')
    remarks = Column(String(255), nullable=True, comment='备注')

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
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
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

    name = Column(String(255), nullable=False, comment='元素名称', index=True)
    location_type = Column(String(255), nullable=True, comment='定位类型')
    location_value = Column(String(255), nullable=True, comment='定位元素值')
    page_id = Column(Integer, nullable=False, comment='关联页面')
    remarks = Column(String(255), nullable=True, comment='备注')

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
            .join(u, u.id == cls.updated_by) \
            .join(User, User.id == cls.created_by) \
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

    name = Column(String(255), nullable=False, comment='用例名', index=True)
    tags = Column(Integer, nullable=True, comment='自动化标记')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    steps = Column(JSON, nullable=True, comment='运行步骤')
    setup_hooks = Column(JSON, nullable=True, comment='前置操作')
    teardown_hooks = Column(JSON, nullable=True, comment='后置操作')
    variables = Column(JSON, nullable=True, comment='变量')
    version = Column(String(255), nullable=False, comment='版本')
    remarks = Column(String(255), nullable=True, comment='备注')

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
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)


class UiSteps(Base):
    """步骤表"""
    __tablename__ = 'ui_steps'

    index = Column(Integer, nullable=False, comment='步骤排序', index=True)
    operation = Column(String(255), nullable=True, comment='操作')
    input_data = Column(String(255), nullable=True, comment='输入数据')
    location_type = Column(String(255), nullable=True, comment='定位元素方式')
    location_value = Column(String(255), nullable=True, comment='定位元素值')
    output = Column(String(255), nullable=True, comment='输出')
    remarks = Column(String(255), nullable=True, comment='备注')
    case_id = Column(Integer, nullable=True, comment='关联ui测试用例')
    version = Column(String(255), nullable=False, comment='版本')


class UiReports(Base):
    """报告表"""
    __tablename__ = 'ui_reports'

    name = Column(String(255), nullable=False, comment='报告名', index=True)
    result = Column(JSON, nullable=False, comment='报告结果')
    project_id = Column(String(255), nullable=True, comment='项目id')
    module_id = Column(String(255), nullable=True, comment='模块id')
    success = Column(Integer(), nullable=True, comment='是否成功')
    status = Column(String(255), nullable=True, comment='状态')
    duration = Column(String(255), nullable=True, comment='执行耗时')
    case_id = Column(Integer(), nullable=True, comment='用例id', index=True)
    remarks = Column(String(255), nullable=True, comment='备注')


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

                name = Column(String(255), nullable=False, comment='报告名', index=True)
                result = Column(JSON, nullable=False, comment='报告结果')
                report_id = Column(Integer, nullable=False, comment='报告id')
                project_id = Column(String(255), nullable=True, comment='项目id', index=True)
                module_id = Column(String(255), nullable=True, comment='模块id', index=True)
                success = Column(Integer(), nullable=True, comment='是否成功')
                status = Column(String(255), nullable=True, comment='状态')
                duration = Column(String(255), nullable=True, comment='执行耗时')
                case_id = Column(Integer(), nullable=True, comment='用例id', index=True)
                remarks = Column(String(255), nullable=True, comment='备注')

            mode_class = ModelClass
            UiReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls
