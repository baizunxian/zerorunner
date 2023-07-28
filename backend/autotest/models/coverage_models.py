# -*- coding: utf-8 -*-
# @author: xiaobai
from sqlalchemy import Column, String, Integer, DECIMAL, BLOB, Text

from autotest.models import Base


class CoverageBackendReport(Base):
    """后端覆盖率报告"""
    __tablename__ = 'coverage_backend_report'

    name = Column(String(64), nullable=False, comment='用户名', index=True)
    coverage_type = Column(Integer(), nullable=False, comment='1 全量， 2 diff 增量')
    new_branches = Column(String(255), nullable=False, comment='新分支或者md5')
    old_branches = Column(String(255), nullable=True, comment='比对分支或者md5')
    package_count = Column(String(255), nullable=False, comment='包数量')
    class_count = Column(String(255), nullable=False, comment='类数据')
    method_count = Column(String(255), nullable=False, comment='方法数据')
    coverage_rate = Column(DECIMAL, nullable=False, comment='覆盖率')


class CoverageClassDetail(Base):
    __tablename__ = 'coverage_class_detail'

    package_name = Column(String(255), nullable=False, comment='包名')
    class_name = Column(String(255), nullable=False, comment='类名')
    class_file_content = Column(Text, nullable=False, comment='class文件内容')
    class_source_path = Column(String(255), nullable=False, comment='class 源码路径')
    class_md5 = Column(String(255), nullable=False, comment='class文件md5')


class CoverageMethodDetail(Base):
    __tablename__ = 'coverage_method_detail'

    name = Column(String(255), nullable=False, comment='包名')
    method_md5 = Column(String(255), nullable=False, comment='类名')
    class_id = Column(Integer, nullable=False, comment='类id')
    params_string = Column(String(255), nullable=False, comment='参数')
