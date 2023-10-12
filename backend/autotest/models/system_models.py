# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from sqlalchemy import String, Text, Integer, DateTime, select, update, Index, JSON, Boolean
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.schemas.system.lookup import LookupQuery, LookupValueQuery
from autotest.schemas.system.roles import RoleQuery
from autotest.schemas.system.user import UserQuery, UserLoginRecordQuery


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    username = mapped_column(String(64), nullable=False, comment='用户名', index=True)
    password = mapped_column(Text, nullable=False, comment='密码')
    email = mapped_column(String(64), comment='邮箱')
    roles = mapped_column(JSON, comment='用户类型')
    status = mapped_column(Integer, comment='用户状态  1 锁定， 0 正常', default=0)
    nickname = mapped_column(String(255), comment='用户昵称')
    user_type = mapped_column(Integer, comment='用户类型 10 管理人员, 20 测试人员', default=20)
    remarks = mapped_column(String(255), comment='用户描述')
    avatar = mapped_column(Text, comment='头像')
    tags = mapped_column(JSON, comment='标签')

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

    path = mapped_column(String(255), nullable=False, comment='菜单路径')
    name = mapped_column(String(255), nullable=False, comment='菜单名称', index=True)
    component = mapped_column(Integer, comment='组件路径')
    title = mapped_column(String(255), comment='title', index=True)
    isLink = mapped_column(Boolean, comment='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    linkUrl = mapped_column(String(255), comment='链接地址')
    isHide = mapped_column(Boolean, default=False, comment='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive = mapped_column(Boolean, default=True, comment='菜单是否缓存')
    isAffix = mapped_column(Boolean, default=False, comment='固定标签')
    isIframe = mapped_column(Boolean, default=False, comment='是否内嵌')
    roles = mapped_column(String(64), default=False, comment='权限')
    icon = mapped_column(String(64), comment='icon', index=True)
    parent_id = mapped_column(Integer, comment='父级菜单id')
    redirect = mapped_column(String(255), comment='重定向路由')
    sort = mapped_column(Integer, comment='排序')
    menu_type = mapped_column(Integer, comment='菜单类型')
    # lookup_id = mapped_column(Integer, comment='数据字典')
    active_menu = mapped_column(String(255), comment='显示页签')
    views = mapped_column(Integer, default=0, comment='访问数')

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

    name = mapped_column(String(64), nullable=False, comment='菜单名称', index=True)
    role_type = mapped_column(Integer, comment='权限类型，10菜单权限，20用户组权限', index=True, default=10)
    menus = mapped_column(String(64), comment='菜单列表', index=True)
    description = mapped_column(Integer, comment='描述')
    status = mapped_column(Integer, comment='状态 10 启用 20 禁用', default=10)

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

    code = mapped_column(String(64), nullable=False, index=True, comment='编码')
    description = mapped_column(String(256), comment='描述')

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
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(User, User.id == cls.updated_by) \
            .order_by(cls.id.desc())

        return await cls.pagination(stmt)

    @classmethod
    async def get_lookup_by_code(cls, code: str):
        stmt = select(cls).where(cls.code == code, cls.enabled_flag == 1)
        return await cls.get_result(stmt)


class LookupValue(Base):
    __tablename__ = 'lookup_value'

    id = mapped_column(Integer, primary_key=True, comment='主键')
    lookup_id = mapped_column(Integer, nullable=False, index=True, comment='所属类型')
    lookup_code = mapped_column(String(32),  index=True, comment='编码')
    lookup_value = mapped_column(String(256), comment='值')
    ext = mapped_column(String(256), comment='拓展1')
    display_sequence = mapped_column(Integer, comment='显示顺序')

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
            .outerjoin(Lookup, cls.lookup_id == Lookup.id) \
            .outerjoin(User, cls.created_by == User.id) \
            .outerjoin(u, cls.updated_by == u.id) \
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

    id = mapped_column(Integer, primary_key=True, comment='主键')
    remote_addr = mapped_column(String(255), comment='用户名称')
    real_ip = mapped_column(String(255), comment='用户名称')
    request = mapped_column(Text, comment='用户名称')
    method = mapped_column(String(255), comment='操作')
    url = mapped_column(String(255), comment='操作')
    args = mapped_column(String(255), comment='操作')
    form = mapped_column(String(255), comment='操作')
    json = mapped_column(Text, comment='操作')
    response = mapped_column(Text, comment='操作')
    endpoint = mapped_column(Text, comment='操作')
    elapsed = mapped_column(Text, comment='操作')
    request_time = mapped_column(DateTime, comment='操作')
    env = mapped_column(String(255), comment='操作')
    employee_code = mapped_column(String(255), comment='操作')
    toekn = mapped_column(String(255), comment='操作')


class MenuViewHistory(Base):
    """访问"""
    __tablename__ = 'menu_view_history'

    menu_id = mapped_column(Integer(), comment='菜单id', index=True)
    remote_addr = mapped_column(String(64), comment='访问ip', index=True)
    user_id = mapped_column(Integer(), comment='访问人', index=True)


class Notify(Base):
    """消息"""
    __tablename__ = 'notify'

    user_id = mapped_column(Integer(), comment='用户id', index=True)
    group = mapped_column(String(64), comment='组')
    message = mapped_column(String(500), comment='消息')
    send_status = mapped_column(Integer(), comment='发送状态，10成功 20 失败')
    read_status = mapped_column(Integer(), comment='消息状态，10未读 20 已读')


class UserLoginRecord(Base):
    __tablename__ = "user_login_record"
    __table_args__ = (
        Index('idx_login_record_code_logintime', 'code', 'login_time'),
    )

    token = mapped_column(String(40), index=True, comment='登陆token')
    code = mapped_column(String(64), index=True, comment='账号')
    user_id = mapped_column(Integer, comment='用户id')
    user_name = mapped_column(String(50), comment='用户名称')
    logout_type = mapped_column(String(50), comment='退出类型')
    login_type = mapped_column(String(50), index=True, comment='登陆方式   扫码  账号密码等')
    login_time = mapped_column(DateTime, index=True, comment='登陆时间')
    logout_time = mapped_column(DateTime, comment='退出时间')
    login_ip = mapped_column(String(30), index=True, comment='登录IP')
    ret_msg = mapped_column(String(255), comment='返回信息')
    ret_code = mapped_column(String(9), index=True, comment='是否登陆成功  返回状态码  0成功')
    address = mapped_column(String(255), comment='地址')
    source_type = mapped_column(String(255), comment='来源')

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
    id = mapped_column(String(60), primary_key=True, autoincrement=False)
    name = mapped_column(String(255), comment='存储的文件名')
    file_path = mapped_column(String(255), comment='文件路径')
    extend_name = mapped_column(String(255), comment='扩展名称', index=True)
    original_name = mapped_column(String(255), comment='原名称')
    content_type = mapped_column(String(255), comment='文件类型')
    file_size = mapped_column(String(255), comment='文件大小')
