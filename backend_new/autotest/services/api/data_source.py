# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:48
import traceback

from pydantic import BaseModel
import typing

from autotest.corelibs import logger
from autotest.exceptions import ParameterError
from autotest.models.api_models import DataSource
from autotest.schemas.api.data_source import SourceQuery, SourceIn, SourceId
from autotest.schemas.base import BaseSchema
from zerorunner.ext.db import DB


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


class DataSourceService:
    @staticmethod
    def get_db_connect(source_id: int, databases: str = None) -> "DB":
        from autotest.models.api_models import DataSource
        source_info = DataSource.get(source_id)
        if not source_info:
            return []
        source_info = jsonable_encoder(source_info)
        if databases:
            source_info.update({"database": databases})
        source_info = SourceInfo(**jsonable_encoder(source_info)).dict()
        source_info['read_timeout'] = 3
        db_info = DB(**source_info)
        return db_info

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

        data = await DataSource.create_or_update(params.dict())
        return data

    @staticmethod
    async def deleted_source(params: SourceId):
        """删除"""
        return await DataSource.delete(params.id)

    @staticmethod
    async def test_connect(params: SourceInfo) -> bool:
        source_info = params.dict()
        source_info['read_timeout'] = 3
        try:
            db_info = DB(**source_info)
            db_info.close()
        except Exception as err:
            logger.error(traceback.format_exc())
            return False
        return True

    @staticmethod
    def get_db_list(source_id: int):
        """获取数据库列表"""
        db_info = DataSourceService.get_db_connect(source_id)
        data = db_info.execute("show databases;")
        db_list = []
        for db in data:
            db_list.append({"name": db.get("Database", None), "hasChildren": True, "type": "database"})
        return db_list

    @staticmethod
    def get_table_list(source_id: int, databases: str):
        """获取数据库表列表"""
        db_info = DataSourceService.get_db_connect(source_id, databases)
        data = db_info.execute(f"show tables from {databases};")
        table_list = []
        for table in data:
            table_list.append({"name": table.get(f"Tables_in_{databases}", None), "type": "table"})
        return table_list

    @staticmethod
    def get_column_list(source_id: int, databases: str):
        """获取数据库表字段"""
        sql = f"""SELECT TABLE_NAME AS "table_name", COLUMN_NAME AS 'column_name', DATA_TYPE AS "data_type" FROM information_schema.COLUMNS  WHERE TABLE_SCHEMA = '{databases}';"""
        db_info = DataSourceService.get_db_connect(source_id, databases)
        data = db_info.execute(sql)
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
    def execute(params: ExecuteParam):
        """执行语句"""
        db_info = DataSourceService.get_db_connect(params.source_id, params.database)
        data = db_info.execute(params.sql)
        return data
