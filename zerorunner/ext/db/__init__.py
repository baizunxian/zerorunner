# -*- coding: utf-8 -*-
# @author: xiaobai

import pymysql
from pymysql import DatabaseError


class DB:
    def __init__(self, host, port, user, password, database=None, read_timeout=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.read_timeout = read_timeout
        self.charset = 'UTF8MB4'
        self.connect = self.db_connect()
        self.cs = self.db_cursor()

    def db_connect(self):
        """连接初始化"""
        try:
            connect = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                read_timeout=self.read_timeout
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
        self.cs.close()
        self.connect.close()

    def __del__(self):
        self.close()
