# -*- coding: utf-8 -*-
# @author: xiaobai
import datetime
import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, text, Row
from sqlalchemy.orm import sessionmaker, DeclarativeMeta


class DBEngine(object):
    def __init__(self, db_uri: str):
        """
        db_uri = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4'

        """
        engine = create_engine(db_uri)
        self.session = sessionmaker(bind=engine)()

    @staticmethod
    def value_decode(row: dict):
        """
        Try to decode value of table
        datetime.datetime-->string
        datetime.date-->string
        json str-->dict
        :param row:
        :return:
        """
        for k, v in row.items():
            if isinstance(v, datetime.datetime):
                row[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, datetime.date):
                row[k] = v.strftime("%Y-%m-%d")
            elif isinstance(v, str):
                try:
                    row[k] = json.loads(v)
                except ValueError:
                    pass

    def _fetch(self, query: str, size: int = -1, commit: bool = True):
        query = query.strip()
        result = self.session.execute(text(query))
        self.session.commit()
        if query.upper()[:6] == "SELECT":
            if size < 0:
                al = result.fetchall()
                al = DBEngine.default_serialize(al)
                # for el in al:
                #     self.value_decode(el)
                return al or None
            elif size == 1:
                on = dict(result.fetchone())
                self.value_decode(on)
                return on or None
            else:
                mny = result.fetchmany(size)
                mny = [dict(el) for el in mny]
                for el in mny:
                    self.value_decode(el)
                return mny or None
        elif query.upper()[:6] in ("UPDATE", "DELETE", "INSERT"):
            return {"rowcount": result.rowcount}

    @staticmethod
    def default_serialize(obj):
        """默认序序列化"""
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(obj, Row):
                return {key: DBEngine.default_serialize(value) for key, value in
                        dict(zip(obj._fields, obj._data)).items()}
            if isinstance(obj, list):
                return [DBEngine.default_serialize(e) for e in obj]
            if hasattr(obj, "__class__") and isinstance(obj.__class__, DeclarativeMeta):
                return {c.name: DBEngine.default_serialize(getattr(obj, c.name)) for c in obj.__table__.columns}
            return obj
        except TypeError as err:
            return repr(obj)

    def fetchone(self, query, commit=True):
        return self._fetch(query, size=1, commit=commit)

    def fetchmany(self, query, size, commit=True):
        return self._fetch(query=query, size=size, commit=commit)

    def fetchall(self, query, commit=True):
        return self._fetch(query=query, size=-1, commit=commit)

    def insert(self, query, commit=True):
        return self._fetch(query=query, commit=commit)

    def delete(self, query, commit=True):
        return self._fetch(query=query, commit=commit)

    def update(self, query, commit=True):
        return self._fetch(query=query, commit=commit)

    def close(self):
        if self.session:
            self.session.close()


if __name__ == "__main__":
    # db = DBEngine("mysql+pymysql://xxxxx:xxxxx@10.0.0.1:3306/dbname?charset=utf8mb4")
    db = DBEngine("sqlite:////Users/xxx/HttpRunner/examples/data/sqlite.db")
    print(db.fetchmany("""
    select* from student""", 5))
    print(db.fetchmany("select* from student", 5))
