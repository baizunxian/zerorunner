# -*- coding: utf-8 -*-
# @author: 小白
import re
import typing

from loguru import logger
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete, func, text, Select, Insert, \
    Update, Delete, TextClause
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.expression import ClauseList
from sqlalchemy.engine import ResultProxy
from sqlalchemy.orm import class_mapper
from decimal import Decimal
from datetime import datetime, date, time
from contextlib import contextmanager
from typing import Union, Dict, List, Any, Optional

from urllib import parse

class DBUtil:
    def __init__(self, db_url: str = None,
                 host: str = None,
                 port: int = None,
                 username: str = None,
                 password: str = None,
                 database: str = None,
                 driver: str = "mysql+pymysql"):
        """
        Initialize with either a full db_url or individual connection parameters.

        Args:
            db_url: Complete database URL (e.g., "postgresql://user:pass@host:port/dbname")
            host: Database server host
            port: Database server port
            username: Database username
            password: Database password
            database: Database name
            driver: Database driver (default: "postgresql")
        """
        if db_url is None:
            if not all([host, port, username, password]):
                raise ValueError(
                    "Either db_url or all connection parameters (host, port, username, password, database) must be provided")
            db_url = f"{driver}://{username}:{parse.quote(password, safe='')}@{host}:{port}/{database}"

        self._engine = create_engine(
            url=db_url,
            echo=False,
            pool_size=10,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=7200,
        )

        self._session_maker = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        self._session = scoped_session(self._session_maker)
        self._metadata = MetaData()

    def get_table(self, table_name: str) -> Table:
        """获取指定表的 Table 对象"""
        # 如果元数据中还没有这个表，则反射它
        if table_name not in self._metadata.tables:
            with self._engine.begin() as conn:
                self._metadata.reflect(bind=conn, only=[table_name])

        if table_name not in self._metadata.tables:
            raise ValueError(f"Table '{table_name}' not found in database.")
        return self._metadata.tables[table_name]

    @staticmethod
    def get_table_columns(table, exclude: set = None) -> ClauseList:
        """
        获取模型所有字段
        exclude: 排除字段  {"name"}
        :return:
        """
        exclude = exclude if exclude else set()
        return ClauseList(*[i for i in table.columns if i.name not in exclude])

    @staticmethod
    def get_exec_sql(
            sql: Union[str, text, Select, Insert, Update, Delete],
            default_limit: int = 100
    ) -> Union[str, Select, Insert, Update, Delete, text]:
        """
        获取安全的执行SQL，强制WHERE条件检查并自动添加LIMIT

        参数:
            sql: 输入的SQL语句或SQLAlchemy对象
            params: 参数字典
            default_limit: 默认限制行数

        返回:
            处理后的SQL语句或SQLAlchemy对象

        异常:
            ValueError: 当UPDATE/DELETE没有WHERE条件时抛出
        """
        # 处理字符串类型的SQL
        if isinstance(sql, str):
            sql_text = sql.strip().upper()

            # 检查UPDATE/DELETE是否缺少WHERE条件
            if any(cmd in sql_text for cmd in ("UPDATE ", "DELETE ")) and " WHERE " not in sql_text:
                raise ValueError("UPDATE/DELETE 语句必须包含 WHERE 条件")

            # 处理SELECT语句的LIMIT
            if sql_text.startswith("SELECT ") and " LIMIT " not in sql_text:
                original_sql = sql.strip()
                if original_sql.endswith(';'):
                    original_sql = original_sql[:-1]
                return text(f"{original_sql} LIMIT {default_limit}")

            return text(sql)

        # 处理SQLAlchemy Select查询
        elif isinstance(sql, Select):
            if not hasattr(sql._limit, 'value') or sql._limit is None:
                return sql.limit(default_limit)
            return sql

        # 处理SQLAlchemy Update/Delete语句
        elif isinstance(sql, (Update, Delete)):
            # 检查是否有WHERE条件
            if sql.whereclause is None:
                raise ValueError(f"{type(sql).__name__} 语句必须包含 WHERE 条件")
            return sql

        # 处理其他SQLAlchemy语句（如Insert）
        else:
            return sql

    @staticmethod
    def get_sql_type(stmt):
        """获取执行sql类型"""
        if isinstance(stmt, (str, TextClause)):
            # For text SQL, remove comments and get first meaningful word
            sql_text = stmt.text if isinstance(stmt, TextClause) else stmt
            # Remove /* */ comments
            no_comments = re.sub(r'/\*.*?\*/', '', sql_text, flags=re.DOTALL)
            # Remove -- comments
            no_comments = re.sub(r'--.*$', '', no_comments, flags=re.MULTILINE)
            # Get first non-empty word
            first_word = no_comments.strip().split()[0].upper() if no_comments.strip() else None
            return first_word
        else:
            # SQLAlchemy object - use class name
            return type(stmt).__name__.upper()

    def execute_sql(
            self,
            sql: Union[str, text, Select, Insert, Update, Delete],
            params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """执行任意 SQL 语句（查询或 DML）"""
        with self._session() as session:
            sql = self.get_exec_sql(sql)
            self.get_compiled_sql(sql)

            # 执行SQL
            result = session.execute(sql, params or {})

            # 根据SQL类型返回不同结果
            if isinstance(sql, (str, TextClause)):
                # 字符串SQL需要解析类型
                sql_text = sql.text if isinstance(sql, TextClause) else sql
                sql_type = self.get_sql_type(sql_text)
            else:
                # SQLAlchemy对象直接判断类型
                sql_type = type(sql).__name__.upper()

            # 处理不同SQL类型的结果
            if sql_type in ("SELECT", "WITH"):
                # 查询返回结果集
                return [dict(row) for row in result.mappings()]
            elif sql_type == "INSERT":
                # 插入返回影响行数和最后ID
                rowcount = result.rowcount
                last_id = result.inserted_primary_key
                return {"rowcount": rowcount, "lastrowid": last_id[0] if last_id else None}
            elif sql_type in ("UPDATE", "DELETE"):
                # 更新/删除返回影响行数
                return {"rowcount": result.rowcount}
            else:
                # 其他操作如CREATE TABLE等
                session.commit()
                return {"message": "Operation completed successfully"}
            return result

    def execute_orm(
            self,
            statement,
            params=None,
            commit: bool = False
    ) -> Any:
        """
        执行ORM语句（支持select/insert/update/delete）
        """
        with self._session() as session:
            if statement is not None:
                result = session.execute(statement, params or {})
            if commit:
                session.commit()
            return result if statement is not None else None

    def fetch_all(
            self,
            sql: Union[str, text, Select],
            params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """执行查询并返回所有结果"""
        result = self.execute_sql(sql, params)
        return [dict(row) for row in result.fetchall()]

    def fetch_one(
            self,
            sql: Union[str, text, Select],
            params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict]:
        """执行查询并返回一条记录"""
        result = self.execute_sql(sql, params)
        row = result.fetchone()
        return dict(row) if row else None

    def execute(
            self,
            sql: Union[str, text, Insert, Update, Delete],
            params: Optional[Dict[str, Any]] = None
    ) -> int:
        """执行插入/更新/删除语句，返回影响行数"""
        result = self.execute_sql(sql, params)
        return result.rowcount

    def handle_data(
            self,
            table_name: str,
            data: Union[List[Dict[str, Any]], Dict[str, Any]]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        处理数据，过滤掉表中不存在的字段和值为None的字段
        """
        # 获取表结构
        table = self.get_table(table_name)
        table_columns = set(table.columns.keys())

        def filter_item(item: Dict[str, Any]) -> Dict[str, Any]:
            """过滤单个字典项"""
            return {
                k: v
                for k, v in item.items()
                if v is not None and k in table_columns
            }

        if isinstance(data, dict):
            return filter_item(data)
        elif isinstance(data, list):
            return [filter_item(item) for item in data]
        else:
            raise ValueError("Invalid data type. Expected list or dict.")

    def insert(
            self,
            table_name: str,
            data: Dict[str, Any],
            return_inserted: bool = True
    ) -> Union[int, Dict[str, Any]]:
        """
        插入数据到指定表
        """
        table = self.get_table(table_name)
        data = self.handle_data(table_name, data)
        stmt = insert(table).values(**data)

        if return_inserted:
            # 获取插入后的完整数据
            with self._session() as session:
                result = session.execute(stmt)
                session.commit()
                (primary_key,) = result.inserted_primary_key
                inserted_row = self.fetch_one(select(table).where(table.c.id == primary_key))
                return dict(inserted_row) if inserted_row else None
        else:
            # 只返回影响行数
            result = self.execute_sql(stmt)
            return result.rowcount

    def update(self, table_name: str, where_clause: Dict[str, Any], data: Dict[str, Any]) -> int:
        """更新指定条件的数据"""
        table = self.get_table(table_name)
        data = self.handle_data(table_name, data)
        stmt = update(table).where(*[getattr(table.c, k) == v for k, v in where_clause.items()]).values(**data)
        result = self.execute_sql(stmt)
        return result.rowcount

    def delete(self, table_name: str, where_clause: Dict[str, Any]) -> int:
        """删除指定条件的数据"""
        table = self.get_table(table_name)
        stmt = delete(table).where(*[getattr(table.c, k) == v for k, v in where_clause.items()])
        result = self.execute_sql(stmt)
        return result.rowcount

    @staticmethod
    def get_compiled_sql(statement):
        """
        获取替换后的 SQL 语句
        """
        str_sql = str(statement.compile(dialect=psycopg2.dialect(), compile_kwargs={"literal_binds": True}))
        logger.debug(f"get_compiled_sql {str_sql}")
        return str_sql

    def fetch_paginated(
            self,
            sql: Union[str, text, Select],
            params: Optional[Dict[str, Any]] = None,
            page: int = None,
            page_size: int = None,
            count_sql: Optional[Union[str, text, Select]] = None
    ) -> Dict[str, Any]:
        """
        执行分页查询
        """
        # This implementation would be similar to the async version but with synchronous calls
        # Removed FastAPI specific code for better reusability

        if page is None:
            page = 1
        if page_size is None:
            page_size = 10

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10

        # 计算偏移量
        offset = (page - 1) * page_size

        # 构建分页SQL
        if isinstance(sql, str):
            paginated_sql = text(f"{sql} LIMIT :limit OFFSET :offset")
            params = params or {}
            params.update({"limit": page_size, "offset": offset})
        elif isinstance(sql, Select):
            paginated_sql = sql.limit(page_size).offset(offset)
        else:
            paginated_sql = sql

        # 获取总记录数
        if count_sql is None:
            if isinstance(sql, str):
                count_sql = text(f"SELECT COUNT(*) FROM ({sql}) AS total_count")
            elif isinstance(sql, Select):
                count_sql = sql.with_only_columns(*[func.count().label("count")]).order_by(None)
                DBUtil.get_compiled_sql(count_sql)
            else:
                count_sql = sql

        # 执行查询和计数
        data = self.fetch_all(paginated_sql, params)
        count_result = self.fetch_one(count_sql, params)

        total = count_result["count"] if "count" in count_result else list(count_result.values())[0]
        total = int(total)

        # 计算总页数
        total_pages = (total + page_size - 1) // page_size

        return {
            "rows": self.serialize_result(data),
            "rowTotal": total,
            "page": page,
            "pageSize": page_size,
            "pageTotal": total_pages
        }

    def serialize_result(
            self,
            result: Union[ResultProxy, List, Dict, Any],
            date_format: str = "%Y-%m-%d",
            datetime_format: str = "%Y-%m-%d %H:%M:%S",
            time_format: str = "%H:%M:%S"
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], Any]:
        """
        将查询结果序列化为字典格式
        """

        def serialize_value(value: Any) -> Any:
            """序列化单个值"""
            if value is None:
                return None
            elif isinstance(value, (datetime, date, time,)):
                return value.strftime(datetime_format if isinstance(value, datetime)
                                      else date_format if isinstance(value, date)
                else time_format)
            elif isinstance(value, Decimal):
                return float(value)
            elif isinstance(value, (list, tuple)):
                return [serialize_value(v) for v in value]
            elif isinstance(value, dict):
                return {k: serialize_value(v) for k, v in value.items()}
            elif hasattr(value, '__dict__'):  # ORM 对象
                return serialize_value(value.__dict__)
            return value

        # 处理 ResultProxy
        if isinstance(result, ResultProxy):
            return [dict(row) for row in result]

        # 处理 RowProxy 或 Row 对象
        if hasattr(result, '_mapping'):
            return dict(result._mapping)

        # 处理 ORM 对象
        if hasattr(result, '__table__'):
            return {c.name: serialize_value(getattr(result, c.name))
                    for c in class_mapper(result.__class__).columns}

        # 处理字典列表
        if isinstance(result, list):
            return [self.serialize_result(row) for row in result]

        # 处理单个字典
        if isinstance(result, dict):
            return {k: serialize_value(v) for k, v in result.items()}

        # 其他类型直接返回
        return serialize_value(result)

    @contextmanager
    def transaction(self):
        """提供事务上下文"""
        with self._session.begin() as session:
            yield session

    def close(self):
        """关闭连接池"""
        self._engine.dispose()
