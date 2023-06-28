# -*- coding: utf-8 -*-
# @author: xiaobai
import datetime
import uuid


def get_str_uuid():
    return str(uuid.uuid4()).replace("-", "")


def get_time(time_type=1, day=0, add_time_unit="days"):
    """
    函数说明：传入时间格式类型（time_type），增加天数（day）生成当前时间字符
    引用函数实参格式：${get_time(1, 0)}，形参：${get_time($time_type, $day)}
    :param time_type: 时间格式类型
    :param day: 增加天数 0为今天，1为明天，-1为昨天
    :param add_time_unit: 增加时间单位
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
