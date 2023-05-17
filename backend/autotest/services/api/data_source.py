# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:48
import traceback

from pydantic import BaseModel, Field
import typing

from loguru import logger
from autotest.exceptions.exceptions import ParameterError
from autotest.schemas.api.data_source import SourceQuery, SourceIn, SourceId
from autotest.schemas.base import BaseSchema
from autotest.models.api_models import DataSource
from autotest.utils.des import encrypt_rsa_password, decrypt_rsa_password
from zerorunner.ext.db import DB, DBConfig


class SourceInfo(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str = None


class ExecuteParam(BaseModel):
    source_id: int
    database: str = ""
    sql: str


class SourceListQuery(BaseSchema):
    id: typing.Optional[typing.Union[str, None]]
    source_type: str = "mysql"
    env_id: typing.Optional[int]
    name: typing.Optional[str]


class SourceSaveSchema(BaseModel):
    id: int = None
    type: str
    name: str
    host: str
    port: str
    user: str
    password: str
    env_id: int


class SourceIdIn(BaseModel):
    source_id: int = Field(None, description="数据源id")


class SourceTableIn(BaseModel):
    source_id: int = Field(None, description="数据源id")
    databases: str = Field(None, description="databases")


class CreateTableIn(BaseModel):
    source_id: int = Field(None, description="数据源id")
    databases: str = Field(None, description="databases")
    table_name: str = Field(None, description="table_name")


class DataSourceService:
    @staticmethod
    async def get_db_connect(source_id: int, database: str = None) -> "DB":
        source_info = await DataSource.get(source_id)
        new_password = decrypt_rsa_password(source_info.password)
        if not source_info:
            raise ValueError("未找到数据源~")
        db_config = DBConfig(host=source_info.host,
                             port=source_info.port,
                             user=source_info.user,
                             password=new_password,
                             database=database,
                             read_timeout=3)
        db_engine = DB(db_config)
        return db_engine

    @staticmethod
    async def get_source_list(params: SourceQuery) -> typing.Dict[str, typing.Any]:
        """获取数据源列表"""
        data = await DataSource().get_list(params)
        return data

    @staticmethod
    async def save_or_update(params: SourceIn) -> typing.Dict[str, typing.Any]:
        """更新保存"""
        if params.id:
            source_info = await DataSource.get(params.id)
            if not source_info:
                raise ParameterError("数据不存在！")
        if params.password:
            params.password = encrypt_rsa_password(params.password)
        data = await DataSource.create_or_update(params.dict())
        return data

    @staticmethod
    async def deleted_source(params: SourceId):
        """删除"""
        return await DataSource.delete(params.id)

    @staticmethod
    async def test_connect(params: SourceInfo) -> bool:
        try:
            db_config = DBConfig(host=params.host,
                                 port=params.port,
                                 user=params.user,
                                 password=params.password,
                                 read_timeout=3)
            db_engine = DB(db_config)
            db_engine.close()
        except Exception as err:
            logger.error(traceback.format_exc())
            return False
        return True

    @staticmethod
    async def get_db_list(params: SourceIdIn):
        """获取数据库列表"""
        db_engine = await DataSourceService.get_db_connect(params.source_id)
        data = db_engine.execute("show databases;")
        db_list = []
        for db in data:
            db_list.append({"name": db.get("Database", None), "hasChildren": True, "type": "database"})
        return db_list

    @staticmethod
    async def get_table_list(params: SourceTableIn):
        """获取数据库表列表"""
        db_engine = await DataSourceService.get_db_connect(params.source_id, params.databases)
        data = db_engine.execute(f"show tables from {params.databases};")
        table_list = []
        for table in data:
            table_list.append({"name": table.get(f"Tables_in_{params.databases}", None), "type": "table"})
        return table_list

    @staticmethod
    async def get_column_list(source_id: int, databases: str):
        """获取数据库表字段"""
        sql = f"""SELECT TABLE_NAME AS "table_name", COLUMN_NAME AS 'column_name', DATA_TYPE AS "data_type" FROM information_schema.COLUMNS  WHERE TABLE_SCHEMA = '{databases}';"""
        db_engine = await DataSourceService.get_db_connect(source_id, databases)
        data = db_engine.execute(sql)
        table_column_list = []
        table_info = {}
        for column in data:
            table_name = column.get("table_name")
            column_name = column.get("column_name")
            data_type = column.get("data_type")
            if table_name not in table_info:
                table_info[table_name] = []
            table_info[table_name].append({"columnName": column_name, "columnType": data_type})
        for key, value in table_info.items():
            table_column_list.append({"tblName": key, "tableColumns": value})
        return table_column_list

    @staticmethod
    async def show_create_table(params: CreateTableIn):
        """查询建表语句"""
        sql = f"""show create table {params.table_name};"""
        db_engine = await DataSourceService.get_db_connect(params.source_id, params.databases)
        data = db_engine.execute(sql)
        data = data[0] if data else {}
        create_table = data.pop("Create Table", "")
        if create_table:
            data['create_table_sql'] = create_table
        return data

    @staticmethod
    async def execute(params: ExecuteParam):
        """执行语句"""
        db_engine = await DataSourceService.get_db_connect(params.source_id, params.database)
        data = db_engine.execute(params.sql)
        return data
