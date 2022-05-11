import traceback
from datetime import datetime
from typing import Any

from flask import request
from loguru import logger
from sqlalchemy import Column, Boolean, DateTime, Integer, func
from sqlalchemy.exc import IntegrityError

from autotest.config import db
from autotest.corelibs.bredis import br
from autotest.exc.consts import TEST_USER_INFO


class Base(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, _commit=True, **kwargs: Any):
        obj = cls(**kwargs)
        obj.save(_commit)
        return obj

    def update(self, _commit=True, **kwargs: Any):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save(_commit)
        return self

    @classmethod
    def get(cls, id, exclude_deleted=True):
        query = db.session.query(cls)
        if hasattr(cls, 'enabled_flag') and exclude_deleted:
            query = query.filter_by(enabled_flag=True)
        return query.filter_by(id=id).first()

    # 分页
    @classmethod
    def paginate(cls, page, per_page, order=None):
        return cls.query.order_by(order).paginate(page, per_page)

    @classmethod
    def all(cls):
        return cls.query.filter(cls.enabled_flag == 1).all()

    def save(self, _commit=True):
        user_info = self.__get_user_token()
        if user_info:
            user_id = user_info.get('id', None)
            if hasattr(self, 'updated_by'):
                setattr(self, 'updated_by', user_id)
            if hasattr(self, 'created_by'):
                if not self.created_by:
                    setattr(self, 'created_by', user_id)
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except IntegrityError:
            logger.error(traceback.format_exc())
            db.session.rollback()
            raise

        _hooks = ('_clean_cache',)
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()

    def execute(self, sql, _commit=True):
        try:
            db.session.execute(sql)
            if _commit:
                db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

        _hooks = ('_clean_cache',)
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()

    def delete(self, _hard=False, _commit=True):
        if hasattr(self, 'enabled_flag') and _hard is False:
            self.enabled_flag = 0
            db.session.add(self)
        else:
            db.session.delete(self)
        if _commit:
            db.session.commit()

        _hooks = ('_clean_cache',)
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()

    def __get_user_token(self):
        """
        根据token获取用户信息
        :return:
        """
        try:
            token = request.headers.get('token')
        except RuntimeError as err:
            logger.debug(f'get user token err：{err}')
            return None
        user_info = br.get(TEST_USER_INFO.format(token))
        return user_info

    @staticmethod
    def save_all(args, _commit=True):
        db.session.add_all(args)
        if _commit:
            db.session.commit()


class TimestampMixin:
    creation_date = Column(DateTime(), default=datetime.now, comment='创建时间')
    created_by = Column(Integer, nullable=True, comment='创建人')
    updation_date = Column(DateTime(), default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    updated_by = Column(Integer, nullable=True, comment='更新人')
    enabled_flag = Column(Boolean(), default=True, nullable=False, comment='是否删除, 0 删除 1 非删除')
