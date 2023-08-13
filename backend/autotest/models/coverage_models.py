# -*- coding: utf-8 -*-
# @author: xiaobai
from sqlalchemy import Column, String, Integer, DECIMAL, BLOB, Text

from autotest.models import Base


class CoverageBackendReport(Base):
    """后端覆盖率报告"""
    __tablename__ = 'coverage_backend_report'

    name = Column(String(64), nullable=False, comment='用户名', index=True)
    coverage_type = Column(Integer(), nullable=False, comment='10 full 全量， 20 diff 增量')
    new_branches = Column(String(255), nullable=False, comment='新分支或者md5')
    old_branches = Column(String(255), nullable=True, comment='比对分支或者md5')
    package_count = Column(String(255), nullable=False, comment='包数量')
    class_count = Column(String(255), nullable=False, comment='类数据')
    method_count = Column(String(255), nullable=False, comment='方法数据')
    coverage_rate = Column(DECIMAL, nullable=False, comment='覆盖率')


class CoverageClassDetail(Base):
    __tablename__ = 'coverage_class_detail'

    report_id = Column(Integer(), nullable=False, comment='报告id')
    package_name = Column(String(255), nullable=False, comment='包名')
    class_name = Column(String(255), nullable=False, comment='类名')
    class_file_content = Column(Text, nullable=False, comment='class文件内容')
    class_source_path = Column(String(255), nullable=False, comment='class 源码路径')
    class_md5 = Column(String(255), nullable=False, comment='class文件md5')
    branch_missed = Column(Integer(), nullable=False, comment='未覆盖分支', default=0)
    branch_covered = Column(Integer(), nullable=False, comment='覆盖分支', default=0)
    instruction_missed = Column(Integer(), nullable=False, comment='未覆盖指令', default=0)
    instruction_covered = Column(Integer(), nullable=False, comment='覆盖指令', default=0)
    line_missed = Column(Integer(), nullable=False, comment='未覆盖行', default=0)
    line_covered = Column(Integer(), nullable=False, comment='覆盖行', default=0)
    complexity_missed = Column(Integer(), nullable=False, comment='未覆盖复杂度', default=0)
    complexity_covered = Column(Integer(), nullable=False, comment='覆盖复杂度', default=0)
    method_missed = Column(Integer(), nullable=False, comment='未覆盖方法', default=0)
    method_covered = Column(Integer(), nullable=False, comment='覆盖方法', default=0)
    class_missed = Column(Integer(), nullable=False, comment='未覆盖类', default=0)
    class_covered = Column(Integer(), nullable=False, comment='覆盖类', default=0)


class CoverageMethodDetail(Base):
    __tablename__ = 'coverage_method_detail'

    report_id = Column(Integer(), nullable=False, comment='报告id')
    name = Column(String(255), nullable=False, comment='包名')
    method_md5 = Column(String(255), nullable=False, comment='类名')
    class_id = Column(Integer, nullable=False, comment='类id')
    params_string = Column(String(255), nullable=False, comment='参数')
    offset = Column(Integer(), nullable=False, comment='偏移量')
    lines_covered_status = Column(String(500), nullable=False, comment='行覆盖状态')
    branch_missed = Column(Integer(), nullable=False, comment='未覆盖分支', default=0)
    branch_covered = Column(Integer(), nullable=False, comment='覆盖分支', default=0)
    instruction_missed = Column(Integer(), nullable=False, comment='未覆盖指令', default=0)
    instruction_covered = Column(Integer(), nullable=False, comment='覆盖指令', default=0)
    line_missed = Column(Integer(), nullable=False, comment='未覆盖行', default=0)
    line_covered = Column(Integer(), nullable=False, comment='覆盖行', default=0)
    complexity_missed = Column(Integer(), nullable=False, comment='未覆盖复杂度', default=0)
    complexity_covered = Column(Integer(), nullable=False, comment='覆盖复杂度', default=0)
    method_missed = Column(Integer(), nullable=False, comment='未覆盖方法', default=0)
    method_covered = Column(Integer(), nullable=False, comment='覆盖方法', default=0)
