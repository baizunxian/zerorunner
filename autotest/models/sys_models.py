from datetime import datetime, timedelta

from sqlalchemy import Column, String, Integer, Text, DateTime, func, distinct
from sqlalchemy.orm import aliased

from .Base import Base, TimestampMixin
from ..config import db


class User(Base, TimestampMixin):
    """用户表"""
    __tablename__ = 'user'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    username = Column(String(64), nullable=False, comment='用户名', index=True)
    password = Column(Text, nullable=False, comment='密码')
    email = Column(String(64), nullable=True, comment='邮箱')
    roles = Column(String, nullable=False, comment='用户类型')
    status = Column(Integer, nullable=False, comment='用户状态', default=0)  # 1 锁定， 0 正常
    nickname = Column(String, nullable=False, comment='用户昵称')
    user_type = Column(String, nullable=False, comment='用户类型', default=20)  # 10 管理人员, 20 测试人员
    remarks = Column(String, nullable=False, comment='用户描述')  # 10 管理人员, 20 测试人员

    @classmethod
    def get_user_by_name(cls, username):
        return User.query.filter(cls.username == username, cls.enabled_flag == 1).first()

    @classmethod
    def get_user_by_nickname(cls, nickname):
        return User.query.filter(cls.nickname == nickname, cls.enabled_flag == 1).first()

    @classmethod
    def get_all_user(cls, username=None, nickname=None, user_ids=None):
        q = []
        if username:
            q.append(cls.username.like('%{}%'.format(username)))
        if nickname:
            q.append(cls.nickname.like('%{}%'.format(nickname)))
        if user_ids and isinstance(user_ids, list):
            q.append(cls.id.in_(user_ids))
        return cls.query.filter(*q, cls.enabled_flag == 1)

    @classmethod
    def get_user_ids(cls, ids=None):
        return cls.query.filter(cls.enabled_flag == 1, cls.id.in_(ids))

    @classmethod
    def get_user_by_roles(cls, roles_id):
        return User.query.filter(cls.roles.like(f'%{roles_id}%'), cls.enabled_flag == 1) \
            .with_entities(cls.id) \
            .all()

    @classmethod
    def get_today_user_login_count(cls, start_time, end_time):
        return cls.query.filter(cls.updation_date.between(start_time, end_time), cls.enabled_flag == 1)


class Menu(Base, TimestampMixin):
    """菜单表"""
    __tablename__ = 'menu'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    path = Column(String(255), nullable=True, comment='菜单路径')
    name = Column(String(255), nullable=True, comment='菜单名称', index=True)
    component = Column(Integer, nullable=True, comment='组件路径')
    title = Column(String(255), nullable=True, comment='title', index=True)
    isLink = Column(Integer, nullable=True, comment='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
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

    @classmethod
    def get_list(cls, env_name=None):
        q = []
        if env_name:
            q.append(cls.env_name.like('%{}%'.format(env_name)))
        return cls.query.filter(*q, cls.enabled_flag == 1)

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.enabled_flag == 1).order_by(cls.sort)

    @classmethod
    def get_menu_by_name(cls, name):
        return cls.query.filter(cls.name == name, cls.enabled_flag == 1).first()

    @classmethod
    def get_menu_by_parent(cls, parent_id):
        return cls.query.filter(cls.parent_id == parent_id, cls.enabled_flag == 1).first()

    @classmethod
    def get_menu_by_ids(cls, ids):
        """获取菜单id"""
        return cls.query.filter(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)

    @classmethod
    def get_parent_id_by_ids(cls, ids):
        """根据子菜单id获取父级菜单id"""
        return cls.query.filter(cls.id.in_(ids), cls.enabled_flag == 1).with_entities(cls.parent_id).distinct().all()


class Roles(Base, TimestampMixin):
    """角色表"""
    __tablename__ = 'roles'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(64), nullable=True, comment='菜单名称', index=True)
    role_type = Column(Integer, nullable=False, comment='权限类型，10菜单权限，20用户组权限', index=True, default=10)
    menus = Column(String(64), nullable=True, comment='菜单列表', index=True)
    description = Column(Integer, nullable=True, comment='描述')
    status = Column(Integer, nullable=True, comment='状态 10 启用 20 禁用', default=10)

    @classmethod
    def get_list(cls, name=None, role_type=10):
        q = list()
        if name:
            q.append(cls.name.like(f'%{name}%'))
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        return cls.query.filter(*q, cls.enabled_flag == 1)

    @classmethod
    def get_all(cls, role_type=10):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.creation_date.desc())

    @classmethod
    def get_roles_by_name(cls, name, role_type=None):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        return cls.query.filter(cls.name == name, *q, cls.enabled_flag == 1).first()

    @classmethod
    def get_menu_by_parent(cls, parent_id, role_type=None):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        return cls.query.filter(cls.parent_id == parent_id, *q, cls.enabled_flag == 1).first()

    @classmethod
    def get_roles_by_ids(cls, ids, role_type=None):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        return cls.query.filter(cls.id.in_(ids), *q, cls.enabled_flag == 1).all()


class Lookup(Base, TimestampMixin):
    __tablename__ = 'lookup'

    id = Column(Integer, primary_key=True, info='主键')
    code = Column(String(64), nullable=False, index=True, info='编码')
    description = Column(String(256), info='描述')

    @classmethod
    def get_list(cls, code=None):
        q = []
        if code:
            q.append(cls.code == code)
        u = aliased(User)
        return cls.query.filter(cls.enabled_flag == 1, *q) \
            .outerjoin(User, cls.created_by == User.id) \
            .outerjoin(u, cls.updated_by == u.id) \
            .with_entities(cls.id,
                           cls.code,
                           cls.description,
                           cls.updated_by,
                           cls.created_by,
                           cls.updation_date,
                           cls.creation_date,
                           u.nickname.label('created_by_name'),
                           User.nickname.label('updated_by_name'),
                           ) \
            .order_by(cls.creation_date.desc())


class LookupValue(Base, TimestampMixin):
    __tablename__ = 'lookup_value'

    id = Column(Integer, primary_key=True, info='主键')
    lookup_id = Column(Integer, nullable=False, index=True, info='所属类型')
    lookup_code = Column(String(32), nullable=False, index=True, info='编码')
    lookup_value = Column(String(256), info='值')
    ext = Column(String(256), info='拓展1')
    display_sequence = Column(Integer, info='显示顺序')

    @classmethod
    def get_lookup_value(cls, code=None, lookup_id=None):
        q = []
        if code:
            q.append(Lookup.code == code)
        if lookup_id:
            q.append(cls.lookup_id == lookup_id)
        u = aliased(User)
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(Lookup, cls.lookup_id == Lookup.id) \
            .outerjoin(User, cls.created_by == User.id) \
            .outerjoin(u, cls.updated_by == u.id) \
            .with_entities(cls.id,
                           cls.lookup_id,
                           cls.lookup_code,
                           cls.lookup_value,
                           cls.ext,
                           cls.display_sequence,
                           cls.updated_by,
                           cls.created_by,
                           cls.updation_date,
                           cls.creation_date,
                           Lookup.code.label('code'),
                           u.nickname.label('created_by_name'),
                           User.nickname.label('updated_by_name'),
                           ) \
            .order_by(cls.display_sequence)

    @classmethod
    def get_lookup_value_by_lookup_id(cls, lookup_id, lookup_code=None):
        q = []
        if lookup_code:
            q.append(cls.lookup_code == lookup_code)
        return cls.query.filter(*q, cls.lookup_id == lookup_id, cls.enabled_flag == 1)


class LogInfo(Base, TimestampMixin):
    __tablename__ = 'log_info'
    id = Column(Integer, primary_key=True, info='主键')
    user_name = Column(String(255), nullable=False, comment='用户名称')
    operation = Column(String(255), nullable=True, comment='操作')
    data_info = Column(Text, nullable=True, comment='数据')

    @classmethod
    def get_list(cls, user_name=None, operation=None, user_ids=None, created_by=None):
        q = []
        if user_name:
            q.append(cls.user_name.like(f'%{user_name}%'))
        if operation:
            q.append(cls.operation.like(f'%{operation}%'))
        if user_ids:
            q.append(cls.created_by.in_(user_ids))
        if created_by:
            q.append(cls.created_by == created_by)

        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .with_entities(cls.id,
                           cls.user_name,
                           cls.operation,
                           cls.data_info,
                           cls.creation_date) \
            .order_by(cls.creation_date.desc())


class RequestHistory(Base, TimestampMixin):
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

    @classmethod
    def get_list(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        elif start_time and not end_time:
            q.append(cls.creation_date >= start_time)
        elif end_time and not start_time:
            q.append(cls.creation_date <= end_time)
        return cls.query.filter(*q, cls.enabled_flag == 1, cls.endpoint.notlike('bigdata.%')) \
            .with_entities(cls.id,
                           func.left(cls.creation_date, 10).label('day_time'),
                           func.left(cls.creation_date, 13).label('hours_time'),
                           func.right(cls.creation_date, 9).label('hours_times'),
                           func.count(cls.id).label('count'),
                           cls.creation_date,
                           cls.endpoint,
                           cls.env)


class MenuViewHistory(Base, TimestampMixin):
    """访问"""
    __tablename__ = 'menu_view_history'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    menu_id = Column(Integer(), nullable=True, comment='菜单id', index=True)
    remote_addr = Column(String(64), nullable=True, comment='访问ip', index=True)
    user_id = Column(Integer(), nullable=True, comment='访问人', index=True)

    @classmethod
    def get_list(cls, start_time=None, end_time=None, select_type='hour'):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        elif start_time and not end_time:
            q.append(cls.creation_date >= start_time)
        hour_rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        day_rows = [1, 2, 3, 4, 5, 6, 7]
        if select_type == 'hour':
            stmts = [db.select([db.cast(db.literal(i), db.String).label("order_hour"), ])
                     for idx, i in enumerate(hour_rows)]
        else:
            now = datetime.now()
            stmts = [db.select([db.cast(func.left(now - timedelta(days=i), 10), db.String).label("order_day"), ])
                     for idx, i in enumerate(day_rows)]

        a = db.union_all(*stmts).subquery()
        b = cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(Menu, cls.menu_id == Menu.id) \
            .with_entities(cls.id,
                           func.count(cls.id).label('count'),
                           func.count(distinct(cls.user_id)).label('user_count'),
                           cls.creation_date,
                           cls.menu_id
                           ).group_by(func.hour(cls.creation_date) if select_type == 'hour'
                                      else func.left(cls.creation_date, 10)).subquery()
        if select_type == 'hour':
            result = db.session.query(a).filter() \
                .outerjoin(b, a.c.order_hour == func.hour(b.c.creation_date)) \
                .with_entities(func.ifnull(b.c.count, 0).label('view_count'),
                               func.ifnull(b.c.user_count, 0).label('user_count'),
                               a.c.order_hour.label('order_hour'),
                               ).order_by(db.cast(a.c.order_hour, db.Integer)).all()
        else:
            result = db.session.query(a).filter() \
                .outerjoin(b, a.c.order_day == db.cast(func.left(b.c.creation_date, 10), db.String)) \
                .with_entities(func.ifnull(b.c.count, 0).label('view_count'),
                               func.ifnull(b.c.user_count, 0).label('user_count'),
                               a.c.order_day.label('order_day'),
                               ).order_by(a.c.order_day).all()

        return result


class Notify(Base, TimestampMixin):
    """消息"""
    __tablename__ = 'notify'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)

    user_id = Column(Integer(), nullable=True, comment='用户id', index=True)
    group = Column(String(64), nullable=True, comment='组')
    message = Column(String(500), nullable=True, comment='消息')
    send_status = Column(Integer(), nullable=True, comment='发送状态，10成功 20 失败')
    read_status = Column(Integer(), nullable=True, comment='消息状态，10未读 20 已读')

    @classmethod
    def get_list(cls, user_id=None, send_status=None, read_status=None):
        q = []
        if user_id:
            q.append(cls.user_id == user_id)
        if send_status:
            q.append(cls.send_status == send_status)
        if read_status:
            q.append(cls.read_status.in_(read_status))

        u = aliased(User)
        return cls.query.filter(*q, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.user_id) \
            .outerjoin(u, u.id == cls.created_by) \
            .with_entities(cls.id,
                           cls.user_id,
                           cls.group,
                           cls.message,
                           cls.send_status,
                           cls.read_status,
                           cls.creation_date,
                           cls.created_by,
                           User.nickname.label('received_user_name'),
                           u.nickname.label('created_user_name'), ) \
            .order_by(cls.creation_date.desc())
