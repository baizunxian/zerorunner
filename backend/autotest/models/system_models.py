# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
import uuid

from sqlalchemy import Column, String, Text, Integer, DateTime, select, update, BigInteger, Index, JSON
from sqlalchemy.orm import aliased

from autotest.models.base import Base
from autotest.schemas.system.lookup import LookupQuery, LookupValueQuery
from autotest.schemas.system.roles import RoleQuery
from autotest.schemas.system.user import UserQuery, UserLoginRecordQuery


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    username = Column(String(64), nullable=False, comment='用户名', index=True)
    password = Column(Text, nullable=False, comment='密码')
    email = Column(String(64), nullable=True, comment='邮箱')
    roles = Column(JSON, nullable=False, comment='用户类型')
    status = Column(Integer, nullable=False, comment='用户状态  1 锁定， 0 正常', default=0)
    nickname = Column(String(255), nullable=False, comment='用户昵称')
    user_type = Column(Integer, nullable=False, comment='用户类型 10 管理人员, 20 测试人员', default=20)
    remarks = Column(String(255), nullable=False, comment='用户描述')
    avatar = Column(Text, nullable=False, comment='头像')
    tags = Column(JSON, nullable=False, comment='标签')

    @classmethod
    async def get_list(cls, params: UserQuery):
        q = [cls.enabled_flag == 1]
        if params.username:
            q.append(cls.username.like('%{}%'.format(params.username)))
        if params.nickname:
            q.append(cls.nickname.like('%{}%'.format(params.nickname)))
        if params.user_ids and isinstance(params.user_ids, list):
            q.append(cls.id.in_(params.user_ids))
        # *[getattr(cls, c.name) for c in cls.__table__.columns]
        u = aliased(User)
        stmt = select(*cls.get_table_columns(), u.nickname.label("created_by_name")) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_user_by_roles(cls, roles_id: int) -> typing.Any:
        stmt = select(cls.id).where(cls.roles.like(f'%{roles_id}%'), cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_name(cls, username: str):
        stmt = select(*cls.get_table_columns()).where(cls.username == username, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_nickname(cls, nickname: str):
        stmt = select(*cls.get_table_columns()).where(cls.nickname == nickname, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)


class Menu(Base):
    """菜单表"""
    __tablename__ = 'menu'

    path = Column(String(255), nullable=False, comment='菜单路径')
    name = Column(String(255), nullable=False, comment='菜单名称', index=True)
    component = Column(Integer, nullable=True, comment='组件路径')
    title = Column(String(255), nullable=True, comment='title', index=True)
    isLink = Column(Integer, nullable=True,
                    comment='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    isHide = Column(Integer, nullable=True, default=False, comment='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive = Column(Integer, nullable=True, default=True, comment='菜单是否缓存')
    isAffix = Column(Integer, nullable=True, default=False, comment='固定标签')
    isIframe = Column(Integer, nullable=True, default=False, comment='是否内嵌')
    roles = Column(String(64), nullable=True, default=False, comment='权限')
    icon = Column(String(64), nullable=True, comment='icon', index=True)
    parent_id = Column(Integer, nullable=True, comment='父级菜单id')
    redirect = Column(String(255), nullable=True, comment='重定向路由')
    sort = Column(Integer, nullable=True, comment='排序')
    menu_type = Column(Integer, nullable=True, comment='菜单类型')
    lookup_id = Column(Integer, nullable=True, comment='数据字典')
    active_menu = Column(String(255), nullable=True, comment='显示页签')
    views = Column(Integer, default=0, nullable=True, comment='访问数')

    @classmethod
    async def get_menu_by_ids(cls, ids: typing.List[int]):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_all(cls):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_by_ids(cls, ids: typing.List[int]):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_all(cls):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_by_title(cls, title: str):
        stmt = select(cls.get_table_columns()).where(cls.title == title, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)
    @classmethod
    async def get_menu_by_name(cls, name: str):
        stmt = select(cls.get_table_columns()).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_menu_by_parent(cls, parent_id: int):
        stmt = select(cls.get_table_columns()) \
            .where(cls.parent_id == parent_id, cls.enabled_flag == 1) \
            .order_by(cls.sort)
        return await cls.get_result(stmt, True)

    @classmethod
    async def add_menu_views(cls, menu_id: int):
        stmt = update(cls.get_table_columns()).where(cls.id == menu_id, cls.enabled_flag == 1).values(
            **{"views": cls.views + 1})
        result = await cls.execute(stmt)
        return result.rowcount


class Roles(Base):
    """角色表"""
    __tablename__ = 'roles'

    name = Column(String(64), nullable=True, comment='菜单名称', index=True)
    role_type = Column(Integer, nullable=False, comment='权限类型，10菜单权限，20用户组权限', index=True, default=10)
    menus = Column(String(64), nullable=True, comment='菜单列表', index=True)
    description = Column(Integer, nullable=True, comment='描述')
    status = Column(Integer, nullable=True, comment='状态 10 启用 20 禁用', default=10)

    @classmethod
    async def get_list(cls, params: RoleQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.role_type:
            q.append(cls.role_type == params.role_type)
        else:
            q.append(cls.role_type == 10)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label("created_by_name"),
                      User.nickname.label("updated_by_name")) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(User, User.id == cls.updated_by) \
            .order_by(cls.id.desc())

        return await cls.pagination(stmt)

    @classmethod
    async def get_roles_by_ids(cls, ids: typing.List, role_type=None):
        q = [cls.enabled_flag == 1, cls.id.in_(ids)]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)

        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_all(cls, role_type=10):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.id.desc())

    @classmethod
    async def get_roles_by_name(cls, name, role_type=None):
        q = [cls.name == name, cls.enabled_flag == 1]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt, True)


class Lookup(Base):
    __tablename__ = 'lookup'

    code = Column(String(64), nullable=False, index=True, comment='编码')
    description = Column(String(256), comment='描述')

    @classmethod
    async def get_list(cls, params: LookupQuery):
        q = [cls.enabled_flag == 1]
        if params.code:
            q.append(cls.code.like(f"%{params.code}%"))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label("created_by_name"),
                      User.nickname.label("updated_by_name")) \
            .where(*q) \
            .join(u, u.id == cls.created_by) \
            .join(User, User.id == cls.updated_by) \
            .order_by(cls.id.desc())

        return await cls.pagination(stmt)

    @classmethod
    async def get_lookup_by_code(cls, code: str):
        stmt = select(cls).where(cls.code == code, cls.enabled_flag == 1)
        return await cls.get_result(stmt)


class LookupValue(Base):
    __tablename__ = 'lookup_value'

    id = Column(Integer, primary_key=True, comment='主键')
    lookup_id = Column(Integer, nullable=False, index=True, comment='所属类型')
    lookup_code = Column(String(32), nullable=False, index=True, comment='编码')
    lookup_value = Column(String(256), comment='值')
    ext = Column(String(256), comment='拓展1')
    display_sequence = Column(Integer, comment='显示顺序')

    @classmethod
    async def get_lookup_value(cls, params: LookupValueQuery = LookupValueQuery()):
        q = [cls.enabled_flag == 1]
        if params.code:
            q.append(Lookup.code == params.code)
        if params.lookup_id:
            q.append(cls.lookup_id == params.lookup_id)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      Lookup.code.label('code'),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name')) \
            .where(*q) \
            .join(Lookup, cls.lookup_id == Lookup.id) \
            .join(User, cls.created_by == User.id) \
            .join(u, cls.updated_by == u.id) \
            .order_by(cls.display_sequence)
        return await cls.get_result(stmt)

    @classmethod
    async def get_lookup_value_by_lookup_id(cls, lookup_id, lookup_code=None):
        q = [cls.lookup_id == lookup_id, cls.enabled_flag == 1]
        if lookup_code:
            q.append(cls.lookup_code == lookup_code)
        stmt = select(cls.get_table_columns()).where(*q) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt, True)


class RequestHistory(Base):
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True, info='主键')
    remote_addr = Column(String(255), nullable=False, comment='用户名称')
    real_ip = Column(String(255), nullable=False, comment='用户名称')
    request = Column(Text, nullable=False, comment='用户名称')
    method = Column(String(255), nullable=True, comment='操作')
    url = Column(String(255), nullable=True, comment='操作')
    args = Column(String(255), nullable=True, comment='操作')
    form = Column(String(255), nullable=True, comment='操作')
    json = Column(Text, nullable=True, comment='操作')
    response = Column(Text, nullable=True, comment='操作')
    endpoint = Column(Text, nullable=True, comment='操作')
    elapsed = Column(Text, nullable=True, comment='操作')
    request_time = Column(DateTime, nullable=True, comment='操作')
    env = Column(String(255), nullable=True, comment='操作')
    employee_code = Column(String(255), nullable=True, comment='操作')
    toekn = Column(String(255), nullable=True, comment='操作')


class MenuViewHistory(Base):
    """访问"""
    __tablename__ = 'menu_view_history'

    menu_id = Column(Integer(), nullable=True, comment='菜单id', index=True)
    remote_addr = Column(String(64), nullable=True, comment='访问ip', index=True)
    user_id = Column(Integer(), nullable=True, comment='访问人', index=True)


class Notify(Base):
    """消息"""
    __tablename__ = 'notify'

    user_id = Column(Integer(), nullable=True, comment='用户id', index=True)
    group = Column(String(64), nullable=True, comment='组')
    message = Column(String(500), nullable=True, comment='消息')
    send_status = Column(Integer(), nullable=True, comment='发送状态，10成功 20 失败')
    read_status = Column(Integer(), nullable=True, comment='消息状态，10未读 20 已读')


class UserLoginRecord(Base):
    __tablename__ = "user_login_record"
    __table_args__ = (
        Index('idx_login_record_code_logintime', 'code', 'login_time'),
    )

    token = Column(String(40), index=True, comment='登陆token')
    code = Column(String(64), index=True, comment='账号')
    user_id = Column(Integer, comment='用户id')
    user_name = Column(String(50), comment='用户名称')
    logout_type = Column(String(50), comment='退出类型')
    login_type = Column(String(50), index=True, comment='登陆方式   扫码  账号密码等')
    login_time = Column(DateTime, index=True, comment='登陆时间')
    logout_time = Column(DateTime, comment='退出时间')
    login_ip = Column(String(30), index=True, comment='登录IP')
    ret_msg = Column(String(255), comment='返回信息')
    ret_code = Column(String(9), index=True, comment='是否登陆成功  返回状态码  0成功')
    address = Column(String(255), comment='地址')
    source_type = Column(String(255), comment='来源')

    @classmethod
    async def get_list(cls, params: UserLoginRecordQuery):
        q = [cls.enabled_flag == 1]
        if params.token:
            q.append(cls.token.like('%{}%'.format(params.token)))
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.user_name:
            q.append(cls.user_name.like('%{}%'.format(params.user_name)))
        u = aliased(User)
        stmt = select(cls) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)


class FileInfo(Base):
    """文件信息"""
    __tablename__ = 'file_info'
    id = Column(String(60), nullable=False, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=True, comment='存储的文件名')
    file_path = Column(String(255), nullable=True, comment='文件路径')
    extend_name = Column(String(255), nullable=True, comment='扩展名称', index=True)
    original_name = Column(String(255), nullable=True, comment='原名称')
    content_type = Column(String(255), nullable=True, comment='文件类型')
    file_size = Column(String(255), nullable=True, comment='文件大小')

