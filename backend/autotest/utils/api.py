import dataclasses
import datetime
import json
from collections import defaultdict
from enum import Enum
from functools import wraps
from math import ceil
from pathlib import PurePath
from types import GeneratorType
from typing import Optional, Any, Dict, Union, Set, Callable, List, Tuple
from flask import request, jsonify, Response, abort
from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE
from autotest.corelibs.bredis import br
from autotest.exc import codes
from autotest.exc.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE, TEST_USER_INFO, CACHE_DAY
from autotest.exc.message import errmsg
from autotest.exc.partner_message import partner_errmsg

SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]


def generate_encoders_by_class_tuples(
        type_encoder_map: Dict[Any, Callable[[Any], Any]]
) -> Dict[Callable[[Any], Any], Tuple[Any, ...]]:
    encoders_by_class_tuples: Dict[Callable[[Any], Any], Tuple[Any, ...]] = defaultdict(
        tuple
    )
    for type_, encoder in type_encoder_map.items():
        encoders_by_class_tuples[encoder] += (type_,)
    return encoders_by_class_tuples


encoders_by_class_tuples = generate_encoders_by_class_tuples(ENCODERS_BY_TYPE)


def jsonable_encoder(
        obj: Any,
        include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        custom_encoder: Optional[Dict[Any, Callable[[Any], Any]]] = None,
        sqlalchemy_safe: bool = True,
) -> Any:
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        encoder = getattr(obj.__config__, "json_encoders", {})
        if custom_encoder:
            encoder.update(custom_encoder)
        obj_dict = obj.dict(
            include=include,  # type: ignore # in Pydantic
            exclude=exclude,  # type: ignore # in Pydantic
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return jsonable_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            custom_encoder=encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        encoded_dict = {}
        for key, value in obj.items():
            if (
                    (
                            not sqlalchemy_safe
                            or (not isinstance(key, str))
                            or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)
                    and ((include and key in include) or not exclude or key not in exclude)
            ):
                encoded_key = jsonable_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    errors: List[Exception] = []
    try:
        data = dict(obj)
    except Exception as e:
        errors.append(e)
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors)
    return jsonable_encoder(
        data,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )


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
    data = json.dumps(jsonable_encoder(dict(code=code, msg=msg, data=data, success=success)))
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
        'result': jsonable_encoder(query.all())
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
