"""
基本函数实现
提供使用中使用的获取随机数，时间等基本方法
"""
import datetime
import math
import random
import time
import uuid

import arrow as arrow


# -----------------------------------  随机  ----------------------------------------------

def get_randint(min_num=0, max_num=100):
    """
    生成指定范围随机整数
    :param min_num: 最小数
    :param max_num: 最大数
    :return: number
    """
    return random.randint(min_num, max_num)


def get_rand(size=5):
    """
    生成指定位数随机数
    :param size:
    :return:
    """
    value = int(random.random() * math.pow(10, size))
    if len(str(value)) < size:
        value = value * math.pow(10, size - len(str(value)))
    return int(value)


def get_rand_chinese(size=1):
    """
    生成指定位数随机中文
    :param size:
    :return:
    """
    rand_str = ''
    for i in range(size):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
        val = f'{head:x}{body:x}'
        rand_str = rand_str + bytes.fromhex(val).decode('gb2312')
    return rand_str


def get_uuid(size=32):
    """
    生成随机字符,默认32位
    :param size:
    :return:
    """
    return str(uuid.uuid1()).replace('-', '')[0:size]


def int_to_str(str):
    """
    数字转字段串，JS超过15位后，精度会丢失，
    :param str:
    :return:
    """
    try:
        return int(str)
    except:
        return str


def sum_number(num1=0, num2=0):
    """
    返回两个数字相加
    :param num1:
    :param num2:
    :return:
    """
    try:
        sum = num1 + num2
    except:
        sum = "参数错误，请检查"
    return sum


# -----------------------------------  时间 ----------------------------------------------
def get_timestamp():
    """
    成当前时间戳
    :return: timestamp
    """
    return int(round(time.time() * 1000))


def time_sleep(seconds=0):
    """
    线程睡眠，对进程挂起,seconds:秒数
    :param seconds:
    :return:
    """
    time.sleep(seconds)


def get_time(time_type=1, day=0, add_time_unit="days"):
    """
    生成当前时间字符
    :param time_type: 时间格式类型 day 增加天数 add_time_unit 增加时间单位
    :param day:
    :param add_time_unit:
    :return:
    """
    format_json = {
        1: '%Y-%m-%d %H:%M:%S',
        2: '%Y-%m-%d %H:%M',
        3: '%Y-%m-%d %H',
        4: '%Y-%m-%d',
        5: '%Y-%m',
        6: '%Y',
        7: '%Y%m%d%H%M%S',
        8: '%Y%m%d%H%M',
        9: '%Y%m%d%H',
        10: '%Y%m%d',
        11: '%Y%m',
        12: '%M',
        13: '%d',
        14: '%H',
        15: '%M',
        16: '%S',
        17: '%Y-%m-%dT%H:%M:%S'
    }

    data_format = format_json.get(time_type)
    if add_time_unit == 'hours':
        return (datetime.datetime.now() + datetime.timedelta(hours=day)).strftime(data_format)
    if add_time_unit == 'minutes':
        return (datetime.datetime.now() + datetime.timedelta(minutes=day)).strftime(data_format)
    if add_time_unit == 'seconds':
        return (datetime.datetime.now() + datetime.timedelta(seconds=day)).strftime(data_format)
    if add_time_unit == 'weeks':
        return (datetime.datetime.now() + datetime.timedelta(weeks=day)).strftime(data_format)

    return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime(data_format)


def get_today_start():
    """获取今天开始时间"""
    now = arrow.utcnow().to("local")
    return now.floor("day").format('YYYY-MM-DD HH:mm:ss')


def get_today_start_timestamp():
    """获取今天开始时间搓"""
    return int(time.mktime(time.strptime(str(get_today_start()), '%Y-%m-%d %H:%M:%S')) * 1000)


def get_today_end():
    """获取今天结束时间"""
    now = arrow.utcnow().to("local")
    return now.ceil("day").format('YYYY-MM-DD HH:mm:ss')


def get_today_end_timestamp():
    """获取今天开始时间搓"""
    return int(time.mktime(time.strptime(str(get_today_end()), '%Y-%m-%d %H:%M:%S')) * 1000)


def get_week_start():
    """获取当前周开始时间"""
    now = arrow.utcnow().to("local")
    return now.floor("week").format('YYYY-MM-DD HH:mm:ss')


def get_week_end():
    """获取当前周结束时间"""
    now = arrow.utcnow().to("local")
    return now.ceil("week").format('YYYY-MM-DD HH:mm:ss')


def get_month_start():
    """获取当前月开始时间"""
    now = arrow.utcnow().to("local")
    return now.floor("month").format('YYYY-MM-DD HH:mm:ss')


def get_month_end():
    """获取当前月结束时间"""
    now = arrow.utcnow().to("local")
    return now.ceil("month").format('YYYY-MM-DD HH:mm:ss')


def get_quarter_start():
    """获取当前季度开始时间"""
    now = arrow.utcnow().to("local")
    return now.floor("quarter").format('YYYY-MM-DD HH:mm:ss')


def get_quarter_end():
    """获取当前季度结束时间"""
    now = arrow.utcnow().to("local")
    return now.ceil("quarter").format('YYYY-MM-DD HH:mm:ss')


def get_year_start():
    """获取当前年开始时间"""
    now = arrow.utcnow().to("local")
    return now.floor("year").format('YYYY-MM-DD HH:mm:ss')


def get_year_end():
    """获取当前年开始时间"""
    now = arrow.utcnow().to("local")
    return now.ceil("year").format('YYYY-MM-DD HH:mm:ss')


# -----------------------------------  redis操作  ----------------------------------------------

def redis_get(key):
    """
    获取key值
    :param key: key
    :return:
    """
    return br.get(key)


def redis_set(key, value, expire=0):
    """
    插入redis值
    :param key: key
    :param value: value
    :param expire: 时效
    :return:
    """
    return br.set(key, value, expire)


def redis_delete(*keys):
    """
    删除key
    :param keys: key 列表
    :return:
    """
    return br.delete(*keys)


# -----------------------------------  db操作  ----------------------------------------------

def db_execute(host, port, user, password, database, sql):
    """
    执行sql语句
    :param host: 数据库地址
    :param port: 端口号
    :param user: 用户名
    :param password: 密码
    :param database: 数据库
    :param sql: sql语句
    :param decrypt: 密码是否加密
    :return:
    """
    db = DB(host, port, user, password, database)
    return db.execute(sql)
