import typing

from sqlalchemy import Integer, String, Text, DateTime, BigInteger, func, \
    distinct, text, and_, JSON, DECIMAL, select, update, Boolean, case
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.api.api_case import ApiCaseQuery
from autotest.schemas.api.api_info import ApiQuery, ApiIds
from autotest.schemas.api.api_report import TestReportQuery, TestReportDetailQuery
from autotest.schemas.api.data_source import SourceQuery
from autotest.schemas.api.env import EnvQuery, BindingDataSourceIn, BindingFuncIn
from autotest.schemas.api.functions import FuncQuery
from autotest.schemas.api.module import ModuleQuery
from autotest.schemas.api.projectquery import ProjectQuery


class ProjectInfo(Base):
    """项目表"""
    __tablename__ = 'project_info'

    name = mapped_column(String(64), nullable=False, comment='项目名称', index=True)
    responsible_name = mapped_column(String(64), comment='负责人')
    test_user = mapped_column(String(100), comment='测试人员')
    dev_user = mapped_column(String(100), comment='开发人员')
    publish_app = mapped_column(String(100), comment='发布应用')
    simple_desc = mapped_column(String(100), comment='简要描述')
    remarks = mapped_column(String(100), comment='其他信息')
    config_id = mapped_column(Integer, comment='关联配置id')
    product_id = mapped_column(Integer, comment='产品线id')

    @classmethod
    async def get_list(cls, params: ProjectQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.id:
            q.append(cls.id == params.id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_project_by_id(cls, id: int):
        stmt = select(cls.get_table_columns()).where(cls.id == id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_project_id_list(cls):
        return cls.query.filter(cls.enabled_flag == 1) \
            .with_entities(cls.id,
                           cls.responsible_name,
                           cls.test_user,
                           cls.dev_user,
                           cls.created_by) \
            .all()

    @classmethod
    async def get_project_by_name(cls, name):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_project_ids(cls):
        return cls.query.filter(cls.enabled_flag == 1).with_entities(cls.id).all()

    @classmethod
    def get_project_by_product_id(cls, product_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.product_id == product_id).with_entities(cls.id).all()


class ModuleInfo(Base):
    """模块表"""
    __tablename__ = 'module_info'

    name = mapped_column(String(64), nullable=False, comment='模块名称', index=True)
    project_id = mapped_column(Integer, comment='归属项目id')
    config_id = mapped_column(Integer, comment='关联配置id')
    test_user = mapped_column(String(100), comment='测试负责人')
    simple_desc = mapped_column(String(100), comment='简要描述')
    remarks = mapped_column(String(100), comment='其他信息')
    module_packages = mapped_column(String(64), comment='模块对应的包名称')
    leader_user = mapped_column(String(100), comment='负责人')
    priority = mapped_column(Integer, comment='默认执行用例优先级', default=4)

    # packages_id = mapped_column(Integer,  comment='包id')

    @classmethod
    async def get_list(cls, params: ModuleQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.project_name:
            q.append(ProjectInfo.name.like('%{}%'.format(params.project_name)))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        # if packages_id:
        #     q.append(cls.packages_id == packages_id)
        if params.sort_type == 0:
            sort_type = 'asc'
        else:
            sort_type = 'desc'
        if not params.order_field or params.order_field == 'creation_date':
            params.order_field = 'module_info.creation_date'
        if params.order_field == 'project_name':
            params.order_field = 'project_info.name'
        if params.order_field == 'test_user':
            params.order_field = 'user.nickname'
        order_by = '{} {} {} {}'.format(params.order_field, sort_type, ',module_info.id', sort_type)
        u = aliased(User)

        stmt = select(cls.get_table_columns(),
                      func.count(distinct(ApiInfo.id)).label('case_count'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name')).where(*q) \
            .outerjoin(ProjectInfo, and_(cls.project_id == ProjectInfo.id, ProjectInfo.enabled_flag == 1)) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ApiInfo, and_(cls.id == ApiInfo.module_id, ApiInfo.enabled_flag == 1)) \
            .group_by(cls.id).order_by(text(order_by))
        return await cls.pagination(stmt)

    @classmethod
    async def get_module_by_project_id(cls, project_id: int):
        """查询项目是否有关联模块"""
        stmt = select(cls.id).where(cls.project_id == project_id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_module_by_name(cls, name: str):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_module_by_id(cls, id):
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    def get_module_by_module_packages(cls, module_packages):
        return cls.query.filter(cls.module_packages == module_packages, cls.enabled_flag == 1).all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_module_by_packages_id(cls, packages_id):
        return cls.query.filter(cls.packages_id == packages_id, cls.enabled_flag == 1).first()


class ApiInfo(Base):
    """接口用例"""
    __tablename__ = 'api_info'

    name = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    module_id = mapped_column(BigInteger, nullable=False, comment='所属模块')
    status = mapped_column(Integer, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code_id = mapped_column(BigInteger, comment='关联接口id')
    code = mapped_column(String(255), comment='接口code')
    priority = mapped_column(Integer, comment='优先级', default=3)
    tags = mapped_column(JSON, comment='用例标签')
    url = mapped_column(String(255), nullable=False, comment='请求地址')
    method = mapped_column(String(255), comment='请求方式')
    remarks = mapped_column(String(255), comment='描述')
    step_type = mapped_column(String(255), comment='描述')
    pre_steps = mapped_column(JSON, comment='前置步骤')
    post_steps = mapped_column(JSON, comment='后置步骤')
    setup_code = mapped_column(Text, comment='前置code')
    teardown_code = mapped_column(Text, comment='后置code')
    setup_hooks = mapped_column(JSON, comment='前置操作')
    teardown_hooks = mapped_column(JSON, comment='后置操作')
    headers = mapped_column(JSON, comment='请求头')
    variables = mapped_column(JSON, comment='变量')
    validators = mapped_column(JSON, comment='断言规则')
    extracts = mapped_column(JSON, comment='提取')
    export = mapped_column(JSON, comment='输出')
    request = mapped_column(JSON, comment='请求参数')

    @classmethod
    async def get_list(cls, params: ApiQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.module_ids:
            q.append(cls.module_id.in_(params.module_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.priority:
            q.append(cls.priority.in_(params.priority))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.api_status:
            q.append(cls.api_status == params.api_status)
        u = aliased(User)

        sort_type = 'asc' if params.sort_type == 0 else 'desc'

        if not params.order_field or params.order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        elif params.order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        elif params.order_field == 'name':
            order_field = 'api_info.name'
        elif params.order_field == 'project_name':
            order_field = 'project_info.name'
        elif params.order_field == 'module_name':
            order_field = 'module_info.name'
        elif params.order_field == 'created_by_name' or params.order_field == 'updated_by_name':
            order_field = 'user.nickname'
        else:
            order_field = 'api_info.id'
        order_by = f'{order_field} {sort_type}'

        stmt = select(cls.id,
                      cls.name,
                      cls.url,
                      cls.method,
                      cls.project_id,
                      cls.module_id,
                      cls.code_id,
                      cls.code,
                      cls.priority,
                      cls.status,
                      cls.tags,
                      cls.updated_by,
                      cls.created_by,
                      cls.updation_date,
                      cls.creation_date,
                      cls.enabled_flag,
                      ProjectInfo.name.label('project_name'),
                      ModuleInfo.name.label('module_name'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')).where(*q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .order_by(text(order_by))

        return await cls.pagination(stmt)

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.enabled_flag == 1, cls.type == 1).all()

    @classmethod
    async def get_api_by_module_id(cls, module_id=None, module_ids=None):
        """查询模块是否有case关联"""
        q = [cls.enabled_flag == 1]
        if module_id:
            q.append(cls.module_id == module_id)
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_api_by_project_id(cls, project_id):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1)

    @classmethod
    async def get_api_by_name(cls, name):
        """获取用例名是否存在"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1, cls.name == name)
        return await cls.get_result(stmt)

    @classmethod
    async def get_api_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_api_by_ids(cls, params: ApiIds):
        if not params.ids:
            return None
        stmt = select(cls.get_table_columns()).where(cls.id.in_(params.ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)

    @classmethod
    def get_api_by_time(cls, start_time, end_time):
        return cls.query.filter(cls.creation_date.between(start_time, end_time), cls.enabled_flag == 1)

    @classmethod
    def statistic_project_api_number(cls):
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectInfo.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)

    @classmethod
    def get_api_by_project_id_or_body(cls, project_id, body_name):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.request.like(('%{}%'.format(body_name))),
                                cls.enabled_flag == 1) \
            .with_entities(cls.id) \
            .all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()


class ApiCaseStep(Base):
    """步骤信息表"""
    __tablename__ = 'api_case_step'
    case_id = mapped_column(BigInteger, nullable=False, comment='用例id')
    source_id = mapped_column(BigInteger, nullable=False, comment='源id')
    name = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    module_id = mapped_column(BigInteger, nullable=False, comment='所属模块')
    status = mapped_column(Integer, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code = mapped_column(String(255), comment='接口code')
    code_id = mapped_column(BigInteger, comment='关联接口id')
    priority = mapped_column(Integer, comment='优先级', default=3)
    url = mapped_column(String(255), nullable=False, comment='请求地址')
    method = mapped_column(String(255), comment='请求方式')
    tags = mapped_column(JSON, comment='用例标签')
    remarks = mapped_column(String(255), comment='描述')
    step_type = mapped_column(String(255), comment='描述')
    pre_steps = mapped_column(JSON, comment='前置步骤')
    post_steps = mapped_column(JSON, comment='后置步骤')
    setup_code = mapped_column(Text, comment='前置code')
    teardown_code = mapped_column(Text, comment='后置code')
    setup_hooks = mapped_column(JSON, comment='前置操作')
    teardown_hooks = mapped_column(JSON, comment='后置操作')
    headers = mapped_column(JSON, comment='请求头')
    variables = mapped_column(JSON, comment='变量')
    validators = mapped_column(JSON, comment='断言规则')
    extracts = mapped_column(JSON, comment='提取')
    export = mapped_column(JSON, comment='输出')
    request = mapped_column(JSON, comment='请求参数')
    step_id = mapped_column(BigInteger, comment='步骤id')
    parent_step_id = mapped_column(BigInteger, comment='父步骤id')
    index = mapped_column(String(255), comment='步骤顺序')
    node_id = mapped_column(String(255), comment='节点id')
    enable = mapped_column(Boolean, default=1, comment='是否启用 0 否 1 是')
    is_quotation = mapped_column(Integer, default=1, comment='是否引用 0 否 1 是')
    version = mapped_column(Integer, default=0, comment='版本号')

    @classmethod
    async def get_list(cls, params: ApiQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.module_ids:
            q.append(cls.module_id.in_(params.module_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.priority:
            q.append(cls.priority.in_(params.priority))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.api_status:
            q.append(cls.api_status == params.api_status)
        u = aliased(User)

        sort_type = 'asc' if params.sort_type == 0 else 'desc'

        if not params.order_field or params.order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        elif params.order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        elif params.order_field == 'name':
            order_field = 'api_info.name'
        elif params.order_field == 'project_name':
            order_field = 'project_info.name'
        elif params.order_field == 'module_name':
            order_field = 'module_info.name'
        elif params.order_field == 'created_by_name' or params.order_field == 'updated_by_name':
            order_field = 'user.nickname'
        else:
            order_field = 'api_info.id'
        order_by = f'{order_field} {sort_type}'

        stmt = select(cls.id,
                      cls.name,
                      cls.url,
                      cls.method,
                      cls.project_id,
                      cls.module_id,
                      cls.code_id,
                      cls.code,
                      cls.priority,
                      cls.status,
                      cls.tags,
                      cls.updated_by,
                      cls.created_by,
                      cls.updation_date,
                      cls.creation_date,
                      cls.enabled_flag,
                      ProjectInfo.name.label('project_name'),
                      ModuleInfo.name.label('module_name'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')).where(*q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .order_by(text(order_by))

        return await cls.pagination(stmt)

    @classmethod
    async def get_step_by_case_id(cls, case_id: int, version: int):
        stmt = (select(cls.get_table_columns({"id"}),
                       ApiInfo.name.label('api_name'),
                       ApiInfo.method.label('api_method'),
                       )
                .outerjoin(ApiInfo, and_(ApiInfo.id == cls.source_id, ApiInfo.enabled_flag == 1))
                .where(cls.case_id == case_id,
                       cls.version == version,
                       cls.enabled_flag == 1).order_by(cls.index.asc()))
        return await cls.get_result(stmt)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    async def get_relation_by_api_id(cls, api_id: typing.Union[str, int]):
        """获取关联关系，那些case 使用了对应的api"""
        q = [cls.enabled_flag == 1]
        stmt = select(
            func.any_value(cls.id.label("case_step_id")),
            func.any_value(ApiCase.id).label("id"),
            func.any_value(ApiCase.name).label("name"),
            func.any_value(func.concat('case_', ApiCase.id)).label("relation_id"),
            func.any_value(func.concat('api_', api_id)).label("from_relation_id"),
            func.any_value(func.concat('case_', ApiCase.id)).label("to_relation_id"),
            func.any_value(User.nickname).label("created_by_name"),
            ApiCase.creation_date,
        ) \
            .join(ApiCase, and_(cls.case_id == ApiCase.id,
                                cls.version == ApiCase.version,
                                ApiCase.enabled_flag == 1
                                )) \
            .outerjoin(User, User.id == ApiCase.created_by) \
            .where(*q, cls.source_id == api_id) \
            .group_by(ApiCase.id) \
            .order_by(ApiCase.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_relation_by_case_ids(cls, case_ids: typing.List[typing.Union[str, int]]):
        """获取关联关系，那些case 使用了对应的api"""
        q = [cls.enabled_flag == 1]
        stmt = select(
            func.any_value(cls.id.label("case_step_id")),
            func.any_value(ApiInfo.id).label("id"),
            func.any_value(func.concat('api_', ApiInfo.id)).label("relation_id"),
            func.any_value(func.concat('api_', ApiInfo.id)).label("from_relation_id"),
            func.any_value(func.concat('case_', ApiCase.id)).label("to_relation_id"),
            func.any_value(ApiInfo.name).label("name"),
            func.any_value(ApiInfo.creation_date).label("creation_date"),
            func.any_value(User.nickname).label("created_by_name"),
            func.any_value(ApiCase.creation_date),
        ) \
            .join(ApiCase, and_(cls.case_id == ApiCase.id,
                                cls.version == ApiCase.version,
                                ApiCase.enabled_flag == 1
                                )) \
            .outerjoin(User, User.id == ApiCase.created_by) \
            .outerjoin(ApiInfo, ApiInfo.id == cls.source_id) \
            .where(*q, cls.case_id.in_(case_ids), cls.step_type == 'api')
        return await cls.get_result(stmt)


class ApiCase(Base):
    """测试用例，集合"""
    __tablename__ = 'api_case'

    name = mapped_column(String(64), nullable=False, comment='名称', index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    remarks = mapped_column(String(255), comment='备注')
    headers = mapped_column(JSON, comment='场景请求头')
    variables = mapped_column(JSON, comment='场景变量')
    step_data = mapped_column(JSON, comment='场景步骤')
    step_rely = mapped_column(Integer, comment='步骤依赖  1依赖， 0 不依赖')
    version = mapped_column(Integer(), comment='版本', default=0)

    # todo 目前步骤详情都冗余在单表，后面会拆为独立的表管理

    @classmethod
    async def get_list(cls, params: ApiCaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.created_by:
            q.append(User.nickname.like(f'%{params.created_by}%'))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by_name:
            q.append(User.nickname.like(f'%{params.created_by_name}%'))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)

        stmt = select(cls.id,
                      cls.name,
                      cls.project_id,
                      cls.remarks,
                      cls.created_by,
                      cls.creation_date,
                      cls.updated_by,
                      cls.updation_date,
                      cls.enabled_flag,
                      func.count(distinct(ApiCaseStep.id)).label('step_count'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name')).where(*q) \
            .outerjoin(ApiCaseStep, and_(ApiCaseStep.case_id == cls.id, cls.version == ApiCaseStep.version,
                                         ApiCaseStep.parent_step_id.is_(None))) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .group_by(cls.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_api_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_case_by_ids(cls, ids: typing.List[int]):
        """根据套件ids查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_case_by_name(cls, name: str):
        """根据套件名称查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)

    @classmethod
    def statistic_project_case_number(cls):
        """统计项目用例数量"""
        return cls.query.outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectInfo.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)


class ApiTestReport(Base):
    """报告表"""
    __tablename__ = 'api_test_report'

    name = mapped_column(String(255), nullable=False, comment='报告名称', index=True)
    start_time = mapped_column(DateTime, comment='执行时间')
    duration = mapped_column(String(255), comment='运行耗时')
    case_id = mapped_column(Integer, comment='执行用例id')
    run_mode = mapped_column(String(255), comment='运行模式， api 接口， case 用例')
    run_type = mapped_column(Integer, comment='运行类型， 10 同步， 20 异步，30 定时任务')
    success = mapped_column(Integer, comment='是否成功， True, False')
    run_count = mapped_column(Integer, comment='运行步骤数')
    actual_run_count = mapped_column(Integer, comment='实际步骤数')
    run_success_count = mapped_column(Integer, comment='运行成功数')
    run_fail_count = mapped_column(Integer, comment='运行失败数')
    run_skip_count = mapped_column(Integer, comment='运行跳过数')
    run_err_count = mapped_column(Integer, comment='运行错误数')
    run_log = mapped_column(Text, comment='运行日志')
    project_id = mapped_column(BigInteger, comment='项目id')
    module_id = mapped_column(BigInteger, comment='模块id')
    env_id = mapped_column(Integer, comment='运行环境')
    exec_user_id = mapped_column(Integer, comment='执行人id')
    exec_user_name = mapped_column(String(255), comment='执行人昵称')
    error_msg = mapped_column(Text, comment='错误信息')

    @classmethod
    async def get_list(cls, params: TestReportQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.user_ids:
            q.append(cls.execute_user_id.in_(params.user_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.min_and_max:
            q.append(cls.creation_date.between(*params.min_and_max))
        if params.exec_user_name:
            q.append(cls.exec_user_name.like('%{}%'.format(params.exec_user_name)))
        if params.case_id:
            q.append(cls.case_id == params.case_id)
        stmt = (select(cls.get_table_columns(exclude={"duration"}),
                       func.round(cls.duration, 2).label("duration"))
                .where(*q).order_by(cls.id.desc()))
        return await cls.pagination(stmt)

    @classmethod
    def get_project_by_name(cls, project_name):
        return cls.query.filter(cls.project_name == project_name, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_id(cls, report_id):
        return cls.query.filter(cls.id == report_id, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_time(cls, begin_time, end_time):
        return cls.query.filter(cls.enabled_flag == 1, cls.start_at.between(begin_time, end_time),
                                cls.success.isnot(None)) \
            .with_entities(cls.id,
                           cls.name,
                           cls.start_time,
                           cls.success,
                           cls.run_count,
                           cls.run_success_count,
                           cls.created_by,
                           cls.run_type,
                           cls.run_mode)

    @classmethod
    def statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.outerjoin(User, User.id == cls.execute_user_id) \
            .with_entities(
            func.count(cls.id).label('run_num'),
            User.username.label('employee_code'),
            User.nickname.label('username'),
        ) \
            .filter(cls.enabled_flag == 1,
                    cls.execute_user_id != -1,
                    *q)

    @classmethod
    def get_statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.filter(cls.enabled_flag == 1,
                                cls.execute_user_id != -1,
                                *q) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .with_entities(
            cls.id,
            ProjectInfo.name.label('project_name'),
            func.round(func.sum(func.if_(cls.success, 1, 0)) / func.count(cls.id) * 100, 2).label(
                'pass_rate'),
            func.round(func.sum(cls.successful_use_case) / func.sum(cls.run_test_count) * 100, 2).label(
                'successes_rate'),
        ).group_by(text('project_name'))


class ApiTestReportDetail:
    """报告表"""
    _mapper = {}

    @staticmethod
    def model(id: int):
        # 目前一个表，多个表修改取模数
        table_index = id % 1
        class_name = f'api_test_report_detail_{table_index}'

        mode_class = ApiTestReportDetail._mapper.get(class_name, None)
        if mode_class is None:
            class ModelClass(Base):
                __module__ = __name__
                __name__ = class_name,
                __tablename__ = class_name

                name = mapped_column(String(255), nullable=False, comment='步骤名称', index=True)
                case_id = mapped_column(String(255), comment='用例id')
                success = mapped_column(Integer, comment='是否成功， True, False')
                status = mapped_column(String(255),
                                       comment='步骤状态  success 成功  fail 失败  skip 跳过')
                step_id = mapped_column(String(255), comment='步骤id')
                parent_step_id = mapped_column(String(255), comment='父级步骤id')
                step_type = mapped_column(String(255), comment='步骤类型')
                step_tag = mapped_column(String(255),
                                         comment='步骤标签 pre 前置，post 后置，controller 控制器')
                message = mapped_column(Text, comment='步骤信息')
                variables = mapped_column(JSON, comment='步骤变量')
                env_variables = mapped_column(JSON, comment='环境变量')
                case_variables = mapped_column(JSON, comment='会话变量')
                session_data = mapped_column(JSON, comment='请求会话数据')
                export_vars = mapped_column(JSON, comment='导出变量')
                report_id = mapped_column(Integer, comment='报告id', index=True)
                url = mapped_column(String(255), comment='请求地址')
                method = mapped_column(String(255), comment='请求方法')
                start_time = mapped_column(DateTime, comment='开始时间')
                duration = mapped_column(DECIMAL(), comment='耗时')
                pre_hook_data = mapped_column(JSON, comment='前置步骤')
                post_hook_data = mapped_column(JSON, comment='后置步骤')
                setup_hook_results = mapped_column(JSON, comment='前置hook结果')
                teardown_hook_results = mapped_column(JSON, comment='后置hook结果')
                index = mapped_column(String(255), comment='顺序')
                status_code = mapped_column(Integer, comment='顺序')
                response_time_ms = mapped_column(DECIMAL(), comment='响应耗时')
                elapsed_ms = mapped_column(DECIMAL(), comment='请求耗时')
                log = mapped_column(Text, comment='运行日志')
                exec_user_id = mapped_column(Integer, comment='执行人id')
                exec_user_name = mapped_column(String(255), comment='执行人昵称')
                source_id = mapped_column(BigInteger, comment='源id')

                @classmethod
                async def get_list(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.id)
                    if params.name:
                        q.append(cls.name.like(f"%{params.name}%"))
                    if params.url:
                        q.append(cls.url.like(f"%{params.url}%"))
                    if params.api_name:
                        q.append(ApiInfo.name.like(f"%{params.api_name}%"))
                    if params.step_type:
                        q.append(cls.step_type == params.step_type)
                    if params.status_list:
                        q.append(cls.status.in_(params.status_list))
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)
                    # else:
                    #     q.append(cls.parent_step_id == None)

                    stmt = select(cls.get_table_columns(),
                                  func.if_(ApiTestReport.run_type != 'api', ApiTestReport.name.label("case_name"),
                                           None),
                                  ApiInfo.name.label("api_name"),
                                  ApiInfo.created_by.label('api_created_by'),
                                  User.nickname.label('api_created_by_name'), ).where(*q) \
                        .outerjoin(ApiInfo, ApiInfo.id == cls.source_id) \
                        .outerjoin(ApiTestReport, ApiTestReport.id == cls.report_id) \
                        .outerjoin(User, User.id == ApiInfo.created_by) \
                        .order_by(cls.index)
                    return await cls.pagination(stmt)

                @classmethod
                async def statistics(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1, cls.report_id == params.id]
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)

                    sub_stmt = (select(
                        # 用例
                        # 用例步骤成功数
                        cls.case_id.label("case_id"),
                        func.count(func.if_(cls.case_id.is_not(None), 1, None)).label("case_count_1"),
                        func.sum(func.if_(and_(cls.status == "SUCCESS", cls.case_id.is_not(None)), 1, 0)).label(
                            "case_step_success_count"),
                        # 用例步骤成功数
                        func.sum(func.if_(and_(cls.status != "SUCCESS", cls.case_id.is_not(None)), 1, 0)).label(
                            "case_step_fail_count"),

                        # 步骤 -------------------------------------------------
                        # 总步骤数
                        func.count('*').label("step_count"),
                        func.count(func.if_(cls.status != "SKIP", 1, None)).label("effective_step_count"),
                        # 成功步骤数
                        func.sum(func.if_(and_(cls.status == "SUCCESS", cls.status != "SKIP"), 1, 0)).label(
                            "step_success_count"),
                        # 失败步骤数
                        func.sum(func.if_(cls.status == "FAILURE", 1, 0)).label(
                            "step_fail_count"),
                        # 跳过步骤数
                        func.sum(func.if_(cls.status == "SKIP", 1, 0)).label("step_skip_count"),

                        # 错误步骤数
                        func.sum(func.if_(cls.status == "ERROR", 1, 0)).label("step_error_count"),

                        # 平均请求时长
                        func.round(func.IFNULL(func.avg(cls.elapsed_ms), 0), 2).label("avg_request_time"),
                        # 总执行时长
                        func.sum(cls.duration).label("request_time_count"))
                                .where(*q).group_by(cls.case_id).subquery())

                    stmt = select(
                        func.count(func.if_(sub_stmt.c.case_id.is_not(None), 1, None)).label("case_count"),
                        func.sum(sub_stmt.c.step_count).label("step_count"),
                        func.round(func.avg(sub_stmt.c.avg_request_time), 2).label("avg_request_time"),
                        func.sum(sub_stmt.c.request_time_count).label("request_time_count"),

                        func.sum(
                            func.if_(and_(
                                sub_stmt.c.case_count_1 > 0,
                                sub_stmt.c.case_step_fail_count == 0), 1, 0))
                        .label("case_success_count"),

                        (func.count(func.if_(sub_stmt.c.case_id.is_not(None), 1, None)) - func.sum(
                            func.if_(and_(
                                sub_stmt.c.case_count_1 > 0,
                                sub_stmt.c.case_step_fail_count == 0), 1, 0))).label("case_fail_count"),

                        func.sum(sub_stmt.c.step_success_count).label("step_success_count"),
                        (func.sum(sub_stmt.c.step_fail_count)).label("step_fail_count"),
                        func.sum(sub_stmt.c.step_skip_count).label("step_skip_count"),
                        func.sum(sub_stmt.c.step_error_count).label("step_error_count"),
                        func.round(
                            func.sum(sub_stmt.c.step_success_count) / func.sum(sub_stmt.c.effective_step_count) * 100,
                            2).label("step_pass_rate"),
                        func.round(
                            (func.sum(func.if_(sub_stmt.c.case_step_fail_count == 0, 1, 0))) / func.count(
                                func.if_(sub_stmt.c.case_id.is_not(None), 1, None)) * 100,
                            2).label(
                            "case_pass_rate")
                    )

                    return await cls.get_result(stmt, first=True)

            mode_class = ModelClass
            ApiTestReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls


class Env(Base):
    """环境表"""
    __tablename__ = 'env'

    name = mapped_column(String(255), nullable=False, comment='环境名称', index=True)
    domain_name = mapped_column(String(255), comment='url地址')
    remarks = mapped_column(String(255), comment='说明')
    variables = mapped_column(JSON(), comment='环境变量')
    headers = mapped_column(JSON(), comment='环境请求头')
    data_sources = mapped_column(JSON(), comment='数据源')

    @classmethod
    async def get_list(cls, params: EnvQuery = EnvQuery()):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        u = aliased(User)
        stmt = select(cls.id,
                      cls.name,
                      cls.domain_name,
                      cls.variables,
                      cls.headers,
                      cls.remarks,
                      cls.updated_by,
                      cls.created_by,
                      cls.creation_date,
                      cls.updation_date,
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'), ).where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取环境"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)


class EnvDataSource(Base):
    """环境数据源关联表"""
    __tablename__ = 'env_data_source'

    env_id = mapped_column(Integer, nullable=False, index=True, comment='环境id')
    data_source_id = mapped_column(Integer, nullable=False, index=True, comment='数据源id')

    @classmethod
    async def unbinding_data_source(cls, params: BindingDataSourceIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.data_source_id.in_(params.data_source_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.id,
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      DataSource.name,
                      DataSource.id.label("data_source_id"),
                      DataSource.host,
                      DataSource.port,
                      DataSource.type,
                      DataSource.user,
                      DataSource.updation_date,
                      DataSource.creation_date,
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(DataSource, DataSource.id == cls.data_source_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class EnvFunc(Base):
    """环境数据源管理表"""
    __tablename__ = 'env_func'

    env_id = mapped_column(Integer, nullable=False, index=True, comment='环境id')
    func_id = mapped_column(Integer, nullable=False, index=True, comment='辅助函数id')

    @classmethod
    async def unbinding_funcs(cls, params: BindingFuncIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.func_id.in_(params.func_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.get_table_columns(),
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      Functions.name.label("name"),
                      Functions.remarks.label("remarks"),
                      Functions.content.label("content"),
                      Functions.id.label("func_id"),
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(Functions, Functions.id == cls.func_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class Functions(Base):
    __tablename__ = 'functions'

    name = mapped_column(Integer, nullable=False, comment='name')
    remarks = mapped_column(Integer, comment='备注')
    project_id = mapped_column(Integer, comment='关联项目')
    content = mapped_column(Text, comment='自定义函数内容')
    func_type = mapped_column(String(255), comment='函数类型')
    func_tags = mapped_column(String(255), comment='函数标签')

    @classmethod
    async def get_list(cls, params: FuncQuery):
        q = [cls.enabled_flag == 1]
        if params.project_name:
            q.append(ProjectInfo.name.like(f'%{params.project_name}%'))
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        u = aliased(User)

        stmt = select(cls.get_table_columns(),
                      ProjectInfo.name.label('project_name'),
                      User.nickname.label('updated_by_name'),
                      u.nickname.label('created_by_name'), ).where(*q) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_by_id(cls, id: int):
        stmt = select(cls.get_table_columns(),
                      ProjectInfo.name.label('project_name')).where(cls.enabled_flag == 1, cls.id == id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id)

        return await cls.get_result(stmt, first=True)

    @classmethod
    def get_by_project_id(cls, project_id):
        return cls.query.filter(cls.project_id == project_id).first()


class DataSource(Base):
    """数据源"""
    __tablename__ = 'data_source'

    type = mapped_column(String(255), comment='数据源类型', index=True)
    name = mapped_column(String(255), nullable=False, comment='数据源名称', index=True)
    host = mapped_column(String(255), comment='ip')
    port = mapped_column(String(255), comment='端口')
    user = mapped_column(String(255), comment='用户名')
    password = mapped_column(String(255), comment='密码')

    @classmethod
    async def get_list(cls, params: SourceQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.source_type:
            q.append(cls.type == params.source_type)
        if params.name:
            q.append(cls.name.like(f"%{params.name}%"))
        if params.source_ids and isinstance(params.source_ids, list):
            q.append(cls.id.in_(params.source_ids))
        u = aliased(User)
        stmt = select(cls.get_table_columns(exclude={"password"}),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name'),
                      ).where(*q) \
            .outerjoin(User, cls.updated_by == User.id) \
            .outerjoin(u, cls.created_by == u.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter(cls.username == username, cls.enabled_flag == 1).first()
