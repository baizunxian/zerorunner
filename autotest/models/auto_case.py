from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import aliased

from autotest.models.Base import Base, TimestampMixin
from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.models.sys_models import User


class AutoTestCase(Base, TimestampMixin):
    """自动测试用例"""
    __tablename__ = 'auto_test_case'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    module_id = Column(Integer, nullable=False, comment='模块id', index=True)
    project_id = Column(Integer, nullable=False, comment='归属项目id')
    api_code_id = Column(Integer, nullable=False, comment='api_code_id')
    api_code = Column(Integer, nullable=False, comment='api_code_id')
    batch_id = Column(Integer, nullable=False, comment='报告id')

    @classmethod
    def get_list(cls, api_code=None):
        u = aliased(User)
        q = []
        if api_code:
            q.append(cls.api_code.like(f'%{api_code}%'))
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .with_entities(cls.id,
                           cls.api_code,
                           cls.api_code_id,
                           cls.module_id,
                           cls.project_id,
                           cls.created_by,
                           cls.updated_by,
                           cls.creation_date,
                           cls.updation_date,
                           cls.batch_id,
                           ProjectInfo.project_name,
                           ModuleInfo.module_name,
                           User.nickname.label('created_by_name'),
                           u.nickname.label('updated_by_name')
                           ) \
            .filter(cls.enabled_flag == 1, *q)

    @classmethod
    def get_case_by_api_code(cls, api_code):
        return cls.query.filter(cls.api_code == api_code, cls.enabled_flag == 1).first()
