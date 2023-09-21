# -*- coding: utf-8 -*-
# @author: xiao bai
from sqlalchemy import String, Integer, Text, select, func, BigInteger
from sqlalchemy.orm import aliased, mapped_column

from autotest.models import Base
from autotest.models.system_models import User
from autotest.schemas.coverage.coverage_report import CoverageReportQuery, CoverageListQuery
from autotest.schemas.coverage.repository_manager import RepositoryListQuery


class RepositoryManager(Base):
    """仓库管理"""
    __tablename__ = 'repository_manager'

    name = mapped_column(String(64), nullable=False,  comment='仓库名称', index=True)
    url = mapped_column(String(255),  comment='仓库地址')
    username = mapped_column(String(64),  comment='用户名')
    password = mapped_column(String(64),  comment='密码')

    @classmethod
    async def get_list(cls, params: RepositoryListQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.id:
            q.append(cls.id == params.id)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)


class CoverageBackendReport(Base):
    """后端覆盖率报告"""
    __tablename__ = 'coverage_backend_report'

    name = mapped_column(String(64), nullable=False,  comment='仓库名称', index=True)
    report_type = mapped_column(BigInteger(),  comment='10 full 全量， 20 diff 增量')
    new_branches = mapped_column(String(255),  comment='新分支或者md5')
    new_last_commit_id = mapped_column(String(255),  comment='新分支最后提交id')
    old_branches = mapped_column(String(255), nullable=True, comment='比对分支或者md5')
    old_last_commit_id = mapped_column(String(255), nullable=True, comment='旧分支最后提交id')
    package_count = mapped_column(String(255),  comment='包数量')
    class_count = mapped_column(String(255),  comment='类数据')
    method_count = mapped_column(String(255),  comment='方法数据')
    coverage_rate = mapped_column(String(255),  comment='覆盖率')

    @classmethod
    async def get_list(cls, params: CoverageListQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.id:
            q.append(cls.id == params.id)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)


class CoverageClassDetail(Base):
    __tablename__ = 'coverage_class_detail'

    report_id = mapped_column(BigInteger(),  nullable=False, comment='报告id')
    package_name = mapped_column(String(255),  comment='包名')
    class_name = mapped_column(String(255),  comment='类名')
    class_file_content = mapped_column(Text,  comment='class文件内容')
    class_source_path = mapped_column(String(255),  comment='class 源码路径')
    class_md5 = mapped_column(String(255),  comment='class文件md5')
    # branch_missed = mapped_column(Integer(),  comment='未覆盖分支', default=0)
    # branch_covered = mapped_column(Integer(),  comment='覆盖分支', default=0)
    # instruction_missed = mapped_column(Integer(),  comment='未覆盖指令', default=0)
    # instruction_covered = mapped_column(Integer(),  comment='覆盖指令', default=0)
    # line_missed = mapped_column(Integer(),  comment='未覆盖行', default=0)
    # line_covered = mapped_column(Integer(),  comment='覆盖行', default=0)
    # complexity_missed = mapped_column(Integer(),  comment='未覆盖复杂度', default=0)
    # complexity_covered = mapped_column(Integer(),  comment='覆盖复杂度', default=0)
    # method_missed = mapped_column(Integer(),  comment='未覆盖方法', default=0)
    # method_covered = mapped_column(Integer(),  comment='覆盖方法', default=0)
    class_missed = mapped_column(Integer(),  comment='未覆盖类', default=0)
    class_covered = mapped_column(Integer(),  comment='覆盖类', default=0)

    @classmethod
    async def get_detail_by_report(cls, params: CoverageReportQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]

        stmt = select(
            cls.get_table_columns(exclude={'class_file_content', 'class_source_path', 'class_md5'}),
            func.concat("package").label("el_type"),
            cls.package_name.label("name"),
            func.sum(CoverageMethodDetail.branch_missed).label('branch_missed'),
            func.sum(CoverageMethodDetail.branch_covered).label('branch_covered'),
            (func.sum(CoverageMethodDetail.branch_missed) + func.sum(CoverageMethodDetail.branch_covered)).label(
                'branch_count'),
            func.sum(CoverageMethodDetail.instruction_missed).label('instruction_missed'),
            func.sum(CoverageMethodDetail.instruction_covered).label('instruction_covered'),
            (func.sum(CoverageMethodDetail.instruction_missed) + func.sum(
                CoverageMethodDetail.instruction_covered)).label('instruction_count'),
            func.sum(CoverageMethodDetail.line_missed).label('line_missed'),
            func.sum(CoverageMethodDetail.line_covered).label('line_covered'),
            (func.sum(CoverageMethodDetail.line_missed) + func.sum(CoverageMethodDetail.line_covered)).label(
                'line_count'),
            func.sum(CoverageMethodDetail.complexity_missed).label('complexity_missed'),
            func.sum(CoverageMethodDetail.complexity_covered).label('complexity_covered'),
            (func.sum(CoverageMethodDetail.complexity_missed) + func.sum(
                CoverageMethodDetail.complexity_covered)).label('complexity_count'),
            func.sum(CoverageMethodDetail.method_missed).label('method_missed'),
            func.sum(CoverageMethodDetail.method_covered).label('method_covered'),
            (func.sum(CoverageMethodDetail.method_missed) + func.sum(CoverageMethodDetail.method_covered)).label(
                'method_count'),
            (cls.class_missed + cls.class_covered).label('class_count'),
        ) \
            .where(*q, cls.id == CoverageMethodDetail.class_id) \
            .group_by(cls.package_name) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_detail_by_package(cls, params: CoverageReportQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id, cls.package_name == params.package_name]
        stmt = select(
            cls.get_table_columns(),
            cls.class_name.label("name"),
            func.concat("class").label("el_type"),
            func.sum(CoverageMethodDetail.branch_missed).label('branch_missed'),
            func.sum(CoverageMethodDetail.branch_covered).label('branch_covered'),
            (func.sum(CoverageMethodDetail.branch_missed) + func.sum(CoverageMethodDetail.branch_covered)).label(
                'branch_count'),
            func.sum(CoverageMethodDetail.instruction_missed).label('instruction_missed'),
            func.sum(CoverageMethodDetail.instruction_covered).label('instruction_covered'),
            (func.sum(CoverageMethodDetail.instruction_missed) + func.sum(
                CoverageMethodDetail.instruction_covered)).label('instruction_count'),
            func.sum(CoverageMethodDetail.line_missed).label('line_missed'),
            func.sum(CoverageMethodDetail.line_covered).label('line_covered'),
            (func.sum(CoverageMethodDetail.line_missed) + func.sum(CoverageMethodDetail.line_covered)).label(
                'line_count'),
            func.sum(CoverageMethodDetail.complexity_missed).label('complexity_missed'),
            func.sum(CoverageMethodDetail.complexity_covered).label('complexity_covered'),
            (func.sum(CoverageMethodDetail.complexity_missed) + func.sum(
                CoverageMethodDetail.complexity_covered)).label('complexity_count'),
            func.sum(CoverageMethodDetail.method_missed).label('method_missed'),
            func.sum(CoverageMethodDetail.method_covered).label('method_covered'),
            (func.sum(CoverageMethodDetail.method_missed) + func.sum(CoverageMethodDetail.method_covered)).label(
                'method_count'),
            (cls.class_missed + cls.class_covered).label('class_count'), ) \
            .where(*q, cls.id == CoverageMethodDetail.class_id) \
            .group_by(cls.class_name) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)


class CoverageMethodDetail(Base):
    __tablename__ = 'coverage_method_detail'

    report_id = mapped_column(BigInteger(), nullable=False, comment='报告id')
    name = mapped_column(String(255),nullable=False,  comment='包名')
    method_md5 = mapped_column(String(255),  comment='类名')
    class_id = mapped_column(Integer,  comment='类id')
    params_string = mapped_column(Text,  comment='参数')
    offset = mapped_column(Integer(),  comment='偏移量')
    lines_covered_status = mapped_column(Text,  comment='行覆盖状态')
    branch_missed = mapped_column(Integer(),  comment='未覆盖分支', default=0)
    branch_covered = mapped_column(Integer(),  comment='覆盖分支', default=0)
    instruction_missed = mapped_column(Integer(),  comment='未覆盖指令', default=0)
    instruction_covered = mapped_column(Integer(),  comment='覆盖指令', default=0)
    line_missed = mapped_column(Integer(),  comment='未覆盖行', default=0)
    line_covered = mapped_column(Integer(),  comment='覆盖行', default=0)
    complexity_missed = mapped_column(Integer(),  comment='未覆盖复杂度', default=0)
    complexity_covered = mapped_column(Integer(),  comment='覆盖复杂度', default=0)
    method_missed = mapped_column(Integer(),  comment='未覆盖方法', default=0)
    method_covered = mapped_column(Integer(),  comment='覆盖方法', default=0)

    @classmethod
    async def get_detail_by_class(cls, params: CoverageReportQuery):
        q = [cls.enabled_flag == 1, cls.class_id == params.class_id]

        stmt = select(
            cls.get_table_columns(),
            func.concat("method").label("el_type"),
            (func.sum(cls.branch_missed) + func.sum(cls.branch_covered)).label('branch_count'),
            (func.sum(cls.instruction_missed) + func.sum(cls.instruction_covered)).label('instruction_count'),
            (func.sum(cls.line_missed) + func.sum(cls.line_covered)).label('line_count'),
            (func.sum(cls.complexity_missed) + func.sum(cls.complexity_covered)).label('complexity_count'),
            (func.sum(cls.method_missed) + func.sum(cls.method_covered)).label('method_count'),
        ) \
            .where(*q) \
            .group_by(cls.name) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)
