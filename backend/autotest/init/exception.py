# -*- coding: utf-8 -*-
# @author: xiaobai

import traceback
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.orm.exc import UnmappedInstanceError
from starlette.requests import Request

from autotest.utils.response.codes import CodeEnum
from loguru import logger
from autotest.exceptions.exceptions import IpError, ErrorUser, UserNotExist, SetRedis, AccessTokenFail, IdNotExist, \
    ParameterError
from autotest.utils.response.http_response import resp_400, resp_500, partner_success


def init_exception(app: FastAPI):
    """ 全局异常捕获 """

    @app.exception_handler(IpError)
    async def ip_error_handler(request: Request, exc: IpError):
        """ ip错误(自定义异常) """
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=exc.msg)

    @app.exception_handler(ErrorUser)
    async def error_user_handler(request: Request, exc: ErrorUser):
        """ 错误的用户名或密码(自定义异常) """
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=exc.msg)

    @app.exception_handler(UserNotExist)
    async def user_not_exist_handler(request: Request, exc: UserNotExist):
        """ 用户不存在(自定义异常) """
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=exc.msg)

    @app.exception_handler(IdNotExist)
    async def id_not_exist_handler(request: Request, exc: IdNotExist):
        """ 查询id不存在(自定义异常) """
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=exc.msg)

    @app.exception_handler(SetRedis)
    async def set_redis_handler(request: Request, exc: SetRedis):
        """ Redis存储失败(自定义异常) """
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=exc.msg)

    @app.exception_handler(AccessTokenFail)
    async def access_token_fail_handler(request: Request, exc: AccessTokenFail):
        """"""
        logger.warning(f"{exc.msg}:{exc.code}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return partner_success(code=exc.code, msg=exc.msg)

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """ 添加/更新的数据与数据库中数据冲突 """
        text = f"添加/更新的数据与数据库中数据冲突!"
        logger.warning(f"{text}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}\nerror:{exc.orig}")
        return resp_400(msg=text)

    @app.exception_handler(ProgrammingError)
    async def programming_error_handle(request: Request, exc: ProgrammingError):
        """ 请求参数丢失 """
        logger.error(f"请求参数丢失\nURL:{request.method}-{request.url}\nHeaders:{request.headers}\nerror:{exc}")
        logger.error(traceback.format_exc())
        return resp_400(msg='请求参数丢失!(实际请求参数错误)')

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 请求参数验证异常 """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}-{request.url}\nHeaders:{request.headers}\nerror:{exc.errors()}")
        logger.error(traceback.format_exc())
        return partner_success(code=CodeEnum.PARTNER_CODE_FAIL.code, msg="参数错误")

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """ 内部参数验证异常 """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}-{request.url}\nHeaders:{request.headers}\nerror:{exc.errors()}")
        logger.error(traceback.format_exc())
        return resp_500(msg=exc.errors())

    @app.exception_handler(UnmappedInstanceError)
    async def un_mapped_instance_error_handler(request: Request, exc: UnmappedInstanceError):
        """ 删除数据的id在数据库中不存在 """
        id = request.path_params.get("id")
        text = f"不存在编号为 {id} 的数据, 删除失败!"
        logger.warning(f"{text}\nURL:{request.method}-{request.url}\nHeaders:{request.headers}")
        return resp_400(msg=text)

    @app.exception_handler(ParameterError)
    async def all_exception_handler(request: Request, exc: ParameterError):
        """ 参数错误 """
        logger.error(
            f"参数错误\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return partner_success(code=exc.code, msg=exc.msg)

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """ 捕获全局异常 """
        logger.error(
            f"全局异常\n{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return partner_success(code=CodeEnum.PARTNER_CODE_FAIL.code, msg=str(exc),
                               headers={'Access-Control-Allow-Origin': '*'})
