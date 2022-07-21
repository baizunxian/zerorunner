from datetime import datetime, timedelta

from sqlalchemy import Column, String, Integer, Text, DateTime, func, distinct
from sqlalchemy.orm import aliased

from .Base import Base, TimestampMixin
from ..config import db


class DataSource(Base, TimestampMixin):
    """数据源"""
    __tablename__ = 'data_source'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    type = Column(String(255), nullable=False, comment='数据源类型', index=True)
    name = Column(String(255), nullable=False, comment='数据源名称', index=True)
    host = Column(String(255), nullable=False, comment='ip')
    port = Column(String(255), nullable=True, comment='端口')
    user = Column(String(255), nullable=False, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码')

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter(cls.username == username, cls.enabled_flag == 1).first()
