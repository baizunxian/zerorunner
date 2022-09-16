# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:48
from pydantic import BaseModel
from typing import Optional, Text, Union, Any, List

from autotest.corelibs.exc_db import DB
from autotest.models.tools_models import DataSource
from autotest.serialize.base_serialize import BaseQuerySchema
from autotest.utils.api import jsonable_encoder


class DBInfo(BaseModel):
    host: Text
    port: int
    user: Text
    password: Text
    database: Text = None


class ExecuteParam(BaseModel):
    source_id: int
    sql: Text


class SourceListQuery(BaseQuerySchema):
    id: Optional[Union[Text, None]]
    source_type: Text = "mysql"


class DataSourceService:
    @staticmethod
    def get_db_connect(source_id: int, databases: Text = None) -> "DB":
        source_info = DataSource.get(source_id)
        if not source_info:
            return []
        source_info = jsonable_encoder(source_info)
        if databases:
            source_info.update({"database": databases})
        db_info = DB(**DBInfo(**jsonable_encoder(source_info)).dict())
        return db_info

    @staticmethod
    def get_source_list(**kwargs: Any) -> List[Any]:
        query_data = SourceListQuery(**kwargs)
        source = DataSource().get_list(**query_data.dict(exclude_none=True)).all()
        # source = DataSourceListSchema().dump(source, many=True)
        return source

    @staticmethod
    def get_db_list(source_id: int):
        db_info = DataSourceService.get_db_connect(source_id)
        data = db_info.execute("show databases;")
        db_list = []
        for db in data:
            db_list.append({"name": db.get("Database", None), "hasChildren": True, "type": "database"})
        return db_list

    @staticmethod
    def get_table_list(source_id: int, databases: Text):
        db_info = DataSourceService.get_db_connect(source_id, databases)
        data = db_info.execute(f"show tables from {databases};")
        table_list = []
        for table in data:
            table_list.append({"name": table.get(f"Tables_in_{databases}", None), "type": "table"})
        return table_list

    @staticmethod
    def get_column_list(source_id: int, databases: Text):
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
    def execute(**kwargs: Any):
        param = ExecuteParam(**kwargs)
        db_info = DataSourceService.get_db_connect(param.source_id)
        data = db_info.execute(param.sql)
        return data
