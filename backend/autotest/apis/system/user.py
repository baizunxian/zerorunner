# -*- coding: utf-8 -*-
# @author: xiaobai

from fastapi import APIRouter, Request, Form

from autotest.utils.local import g
from autotest.utils.response.codes import CodeEnum
from autotest.utils.response.http_response import partner_success
from autotest.schemas.system.user import UserLogin, UserQuery, UserIn, UserResetPwd, UserDel
from autotest.services.system.user import UserService

router = APIRouter()


@router.post("/login", description="登录")
async def login(params: UserLogin):
    data = await UserService.login(params)
    return partner_success(data, msg="登录成功！")


@router.post("/logout", description="登出")
async def logout():
    await UserService.logout()
    return partner_success()


@router.post("/list", description="用户列表")
async def user_list(params: UserQuery):
    data = await UserService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="更新保存用户")
async def save_or_update(user_params: UserIn):
    """
    更新保存用户
    :return:
    """
    await UserService.save_or_update(user_params)
    return partner_success()


@router.post('/getUserInfoByToken', description="通过token获取用户信息")
async def get_user_info(request: Request):
    """
    根据token获取用户信息
    :return:
    """
    token = request.headers.get("token", None)
    user_info = await UserService.get_user_info_by_token(token)
    return partner_success(user_info)


@router.post('/userRegister', description="新增用户")
async def user_register(user_info: UserIn):
    data = await UserService.user_register(user_info)
    return partner_success(data)


@router.post('/resetPassword', description="修改密码")
async def reset_password(params: UserResetPwd):
    await UserService.reset_password(params)
    return partner_success()


@router.post('/deleted', description="删除用户")
async def deleted(params: UserDel):
    return partner_success(code=CodeEnum.PARTNER_CODE_FAIL.code, msg='限制删除用户')
    data = await UserService.deleted(params)
    return partner_success(data)


@router.post('/authorizeToken', description="校验token是否有效")
async def authorize_token(request: Request):
    token = request.headers.get("token", None)
    user_info = await UserService.check_token(token)
    return partner_success(user_info)


@router.post('/getMenuByToken', description="根据token获取菜单数据")
async def get_menu_by_token():
    user_info = await UserService.get_menu_by_token(g.token)
    return partner_success(user_info)
