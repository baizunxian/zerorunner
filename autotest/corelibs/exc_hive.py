import decimal
import datetime
import json


class Hive:
    def __init__(self, host, port, database='', username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.database = database
        self.connect = self.db_connect()
        self.cs = self.connect.cursor()

    def db_connect(self):
        """连接初始化"""
        from pyhive import hive
        from pyhive.exc import DatabaseError
        try:
            connect = hive.Connection(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
        except DatabaseError as err:
            raise Exception('数据库连接错误：', err)

        return connect

    def select(self, sql):
        """查询"""
        self.cs.execute(sql)
        data = self.cs.fetchall()
        data_list = []
        row_headers = [x[0] for x in self.cs.description]
        for result in data:
            result_list = []
            for res in result:
                if isinstance(res, datetime.datetime):
                    res = res.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(res, decimal.Decimal):
                    res = float(res)
                result_list.append(res)
            data_list.append(dict(zip(row_headers, result_list)))
        self.close()
        return data_list

    def execute(self, sql):
        """执行sql"""
        sql_check(sql)
        self.cs.execute(sql)
        self.connect.commit()
        self.close()

    def executemany(self, sql, *args):
        """批量执行"""
        self.cs.executemany(sql, *args)
        self.connect.commit()
        self.close()

    def close(self):
        """关闭连接"""
        self.cs.close()
        self.connect.close()


class PrestoDB:
    def __init__(self, host, port=9000, catalog='hive', user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.catalog = catalog
        self.connect = self.db_connect()
        self.cs = self.connect.cursor()

    def db_connect(self):
        """连接初始化"""
        try:
            connect = dbapi.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                catalog=self.catalog
            )
        except exceptions.DatabaseError as err:
            raise Exception('数据库连接错误：', err)

        return connect

    def select(self, sql: str) -> list:
        """查询"""
        sql = sql.replace('"', "'")
        self.cs.execute(sql)
        data = self.cs.fetchall()
        data_list = []
        row_headers = [x[0] for x in self.cs.description]
        for result in data:
            result_list = []
            for res in result:
                if isinstance(res, datetime.datetime):
                    res = res.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(res, decimal.Decimal):
                    res = float(res)
                result_list.append(res)
            data_list.append(dict(zip(row_headers, result_list)))
        self.close()
        return data_list

    def execute(self, sql):
        """执行sql"""
        sql_check(sql)
        self.cs.execute(sql)
        self.connect.commit()
        self.close()

    def executemany(self, sql, *args):
        """批量执行"""
        self.cs.executemany(sql, *args)
        self.connect.commit()
        self.close()

    def close(self):
        """关闭连接"""
        self.cs.close()
        self.connect.close()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # if isinstance(obj, str):
        #     return obj.decode('utf8')
        else:
            return json.JSONEncoder.default(self, obj)


def sql_check(sql):
    if not any([True if i.upper() in sql.upper() else False for i in ['select', 'update', 'delete']]):
        raise RuntimeError("仅支持 'select', 'update', 'delete' 语句")

    if 'UPDATE' in sql or 'DELETE' in sql.upper():
        if 'WHERE' not in sql.upper():
            raise RuntimeError('update, delete 语句必须包含 where 条件')
