import json
import time
import traceback
from datetime import datetime
from functools import wraps

import requests
import sqlalchemy
from flask import request, jsonify, Response, abort
from math import ceil
from requests.cookies import RequestsCookieJar
from ast import literal_eval

from autotest.config import config
from autotest.corelibs.bredis import br
from autotest.exc import codes
from autotest.exc.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE, TEST_USER_INFO, CACHE_DAY, TEST_USER_LOGIN_TIME
from autotest.exc.message import errmsg
from autotest.exc.partner_message import partner_errmsg


auth = config.Authentication


class MyEncoder(json.JSONEncoder):
    # 转换接口测试用例返回错误
    def default(self, obj):
        try:
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            if isinstance(obj, RequestsCookieJar):
                return requests.utils.dict_from_cookiejar(obj)
            if isinstance(obj, sqlalchemy.DECIMAL):
                return float(obj)
            return json.JSONEncoder.default(self, obj)
        except (UnicodeDecodeError, TypeError):
            return repr(obj)


def partner_success(data=None, code=codes.PARTNER_CODE_OK, http_code=codes.HTTP_OK, msg=None, headers={}):
    """
    通用结果返回
    :param data: 返回数据
    :param code: 状态码
    :param http_code: http状态码
    :param msg: 返回消息
    :param headers: 响应头
    :return:
    """
    if msg is None:
        msg = partner_errmsg.get(code, '')

    if data is None:
        data = {}

    success = True if code == codes.PARTNER_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success), cls=MyEncoder)
    return Response(data, status=http_code, content_type='application/json', headers=headers)


def parse_pagination(query):
    """
    统一分页处理
    :param query: query
    :return:
    """
    if request.method == 'POST':
        page = request.json.get('page', DEFAULT_PAGE)
        pageSize = min(request.json.get('pageSize', DEFAULT_PER_PAGE), 1000)
    else:
        page = request.args.get('page', type=int, default=DEFAULT_PAGE)
        pageSize = min(request.args.get('pageSize', type=int, default=DEFAULT_PER_PAGE), 1000)

    count = query.count()
    total_page = int(ceil(float(count) / pageSize))
    pagination = {
        'rowTotal': count,
        'pageSize': pageSize,
        'page': page,
        'pageTotal': total_page,
    }
    if count != 0:
        if page > total_page:
            _abort(http_code=404)
    else:
        return {
            'pagination': pagination,
            'result': []
        }
    query = query.offset(pageSize * (page - 1)).limit(pageSize)
    return {
        'pagination': pagination,
        'result': query.all()
    }


def _abort(http_code=400, result=None, message='', business_code=None):
    """
    错误返回
    :param http_code:
    :param result:
    :param message:
    :param business_code:
    :return:
    """
    if not business_code:
        business_code = http_code
    data = {
        'code': business_code,
        'msg': message,
        'data': result or {},
        'success': False
    }
    abort(Response(jsonify(data), mimetype='application/json', status=http_code))


def http_fail(data=None, code=None, http_code=None, msg=None, headers={}):
    """
    失败返回
    :param data:
    :param code:
    :param http_code:
    :param msg:
    :param headers:
    :return:
    """
    if code is None:
        code = codes.CODE_BAD_REQUEST
    if msg is None:
        msg = errmsg.get(code, '')
    if http_code is None:
        http_code = code
    if data is None:
        data = {}

    success = True if code == codes.PARTNER_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success))
    return Response(data, status=http_code, mimetype='application/json', headers=headers)


def json_required(func):
    """
    此装饰器可以装饰所有post请求 避免处理非json数据报错
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        json_dict = request.get_json()
        if json_dict is None:
            return http_fail(code=codes.HTTP_BAD_REQUEST, msg='json is required')
        return func(*args, **kwargs)

    return wrapper


# 登录校验
def login_verification(func):
    """
    校验用户是否登录，避免没登录导致数据修改问题
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token', None)
        if token is None:
            return partner_success(code=codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL,
                                   msg=partner_errmsg.get(codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL))
        user_info = br.get(TEST_USER_INFO.format(token))
        if not user_info:
            return partner_success(code=codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL,
                                   msg=partner_errmsg.get(codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL))
        # 重置token时间
        br.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)
        return func(*args, **kwargs)

    return wrapper

