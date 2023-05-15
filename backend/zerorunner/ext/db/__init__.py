# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

import pymysql
from pydantic import BaseModel, Field
from pymysql import DatabaseError


class DBConfig(BaseModel):
    host: str = Field(..., description="host")
    port: typing.Union[int, str] = Field(..., description="port")
    user: str = Field(..., description="user")
    password: str = Field(..., description="port")
    database: str = Field(None, description="database")
    read_timeout: int = Field(None, description="read_timeout")
    charset: str = Field("UTF8MB4", description="charset")


class DB:
    def __init__(self, db_config: DBConfig):
        self.db_config = db_config
        self.connect = self.db_connect()
        self.cs = self.db_cursor()

    def db_connect(self):
        """连接初始化"""
        try:
            connect = pymysql.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                user=self.db_config.user,
                password=self.db_config.password,
                database=self.db_config.database,
                charset=self.db_config.charset,
                read_timeout=self.db_config.read_timeout
            )
        except DatabaseError as err:
            raise Exception('数据库连接错误：', err)

        return connect

    def db_cursor(self):
        """游标初始化"""
        return self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def execute(self, sql):
        """执行sql"""
        self.cs.execute(sql)
        data = self.cs.fetchall()
        self.close()
        return data

    def executemany(self, sql, *args):
        """批量执行"""
        self.cs.executemany(sql, *args)
        self.connect.commit()
        self.close()

    def close(self):
        """关闭连接"""
        try:
            self.cs.close()
            self.connect.close()
        except:
            pass

    def __del__(self):
        self.close()
