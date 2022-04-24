import base64
import datetime
import json

import pymysql
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from pymysql import DatabaseError


class DB:
    def __init__(self, host, port, user, password, database=None, decrypt=False):
        if user and isinstance(user, str) and len(user) == 172:
            user = decrypt_rsa_password(bytes(user, encoding='utf8'))
        if host and isinstance(host, str) and len(host) == 172:
            host = decrypt_rsa_password(bytes(host, encoding='utf8'))
        if password and isinstance(password, str) and len(password) == 172:
            password = decrypt_rsa_password(bytes(password, encoding='utf8'))
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.database = database
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
                charset=self.charset
            )
        except DatabaseError as err:
            raise Exception('数据库连接错误：', err)

        return connect

    def db_cursor(self):
        """游标初始化"""
        return self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def select(self, sql):
        """查询"""
        self.cs.execute(sql)
        data = self.cs.fetchall()
        # logger.debug(f'data_list:{data}')
        return data

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

    def __del__(self):
        self.close()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def sql_check(sql):
    if not any([True if i.upper() in sql.upper() else False for i in ['select', 'update', 'delete']]):
        raise RuntimeError("仅支持 'select', 'update', 'delete' 语句")

    if 'UPDATE' in sql or 'DELETE' in sql.upper():
        if 'WHERE' not in sql.upper():
            raise RuntimeError('update, delete 语句必须包含 where 条件')


def decrypt_rsa_password(password):
    """
    密码解密
    :param password:
    :return:
    """
    try:
        private_key = RSA.import_key(PRIVATE_KEY)
        cipher = PKCS1_v1_5.new(private_key)
        text = cipher.decrypt(base64.b64decode(password), b'')
        return text.decode()
    except Exception as err:
        return ''

# 私钥
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC2YZVJzRrn1kyJHZS+7O5/oteOYOkbiNk3ndRLQscgdDf3k+Ra
RomzvHro5w2h6T9A5rd45vM0kyKcBezE/Za1pOKqmeovah1zxxoofQJ8k91ybVFX
YJx99k9ravCMr+wKuCpuuwPe8he10iBZ465vVZ6g5Nbg4gM2PcV7OMVLaQIDAQAB
AoGABgNhutMngjyVcta4omgOhS3jLcjJ8sbrA4Y220w5DhvALc+7XBMejpWmAfMT
8YekAWGsq7CwqjDON7Gge3kRdz7PDwjaPBwkOebD1aYNWDM0TfQiINVxCkZpPoKg
KTpIELQUoD6KMWw8NUwcasqHcz1HCC6DnRYpG3XJXYhdJDECQQDCvQ/tkHOi92He
RioTHSiJd/5TvgPgBH7dqsldT6mwS67EbrWFEiSSRbzref6wv+r8sXb9d436Ltno
4lngQWZZAkEA78FX7EzS/TAV/PDfWh/ncozY9tFqfPNk4w96LVb5wy8oc9M419K9
yLWeSfiBcXK2l+S2XYk49OhuznklZWiLkQJAL1c+1AXV1rxE8oAkIlloTWL6VOlQ
j9kH7mNiaGjBW7ZKWj5/qkXq1hRWBPi3TciaG6wYvS2fOj7BgrfkGXxMoQJBAIbT
zNUHEvPtMcBP2Nr+7BJgILcUZ3UjDw4dqxCKQ+S+xVn1Y5cDXVTcxcpFZM3eu85J
gUCypYQcngug1yXjF/ECQQCBZZAZ+GhpzqwerwqyfNHvrahSrfp14l6STktaCjKy
IR4n5TomCkHRaeXPgn1YVIhz5/LaVZJuKK3eiN2Wbdwy
-----END RSA PRIVATE KEY-----"""
