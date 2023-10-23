#
#
# class DataSourceTest(Base):
#     """数据源"""
#     __tablename__ = 'data_source'
#
#     type = Column(String(255), nullable=False, comment='数据源类型', index=True)
#     name = Column(String(255), nullable=False, comment='数据源名称', index=True)
#     host = Column(String(255), nullable=False, comment='ip')
#     port = Column(String(255), nullable=True, comment='端口')
#     user = Column(String(255), nullable=False, comment='用户名')
#     password = Column(String(255), nullable=False, comment='密码')
#     env_id = Column(Integer, nullable=False, comment='关联环境')
#
#     @classmethod
#     def get_list(cls, id=None, source_type=None, name=None, env_id=None, source_ids=None):
#         q = []
#         if id:
#             q.append(cls.id == id)
#         if source_type:
#             q.append(cls.type == source_type)
#         if name:
#             q.append(cls.name.like(f"%{name}%"))
#         if env_id:
#             q.append(cls.env_id == env_id)
#         if source_ids and isinstance(source_ids, list):
#             q.append(cls.id.in_(source_ids))
#         u = aliased(User)
#         return cls.query.filter(*q, cls.enabled_flag == 1) \
#             .outerjoin(Env, cls.env_id == Env.id) \
#             .outerjoin(User, cls.updated_by == User.id) \
#             .outerjoin(u, cls.created_by == u.id) \
#             .with_entities(cls.id,
#                            cls.type,
#                            cls.name,
#                            cls.host,
#                            cls.port,
#                            cls.user,
#                            cls.env_id,
#                            cls.created_by,
#                            cls.updation_date,
#                            cls.creation_date,
#                            Env.name.label('env_name'),
#                            u.nickname.label('created_by_name'),
#                            User.nickname.label('updated_by_name'),
#                            ).order_by(cls.creation_date.desc())
#
#     @classmethod
#     def get_user_by_name(cls, username):
#         return cls.query.filter(cls.username == username, cls.enabled_flag == 1).first()
