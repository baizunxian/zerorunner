import copy
import traceback
import uuid
from typing import Dict, Union, Any, Text

from flask import request
from loguru import logger

from autotest.corelibs.bredis import br
from autotest.exc import codes
from autotest.exc.consts import TEST_USER_INFO, CACHE_DAY
from autotest.exc.partner_message import partner_errmsg
from autotest.models.sys_models import User, Menu, Roles
from autotest.serialize.sys_serializes.user import (UserListSchema, UserSchema, UserQuery)
from autotest.services.sys_services.menu import MenuService
from autotest.utils.api import parse_pagination, jsonable_encoder
from autotest.utils.des import encrypt_rsa_password, decrypt_rsa_password


class UserService:
    """用户类"""

    @staticmethod
    def login(**kwargs: Any) -> Dict[Text, Any]:
        """
        登录
        :return:
        """
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        if not username and not password:
            raise ValueError(partner_errmsg.get(codes.PARTNER_CODE_PARAMS_FAIL))
        user_info = User.get_user_by_name(username)
        if not user_info:
            raise ValueError(partner_errmsg.get(codes.WRONG_USER_NAME_OR_PASSWORD))
        u_password = decrypt_rsa_password(user_info.password)

        if u_password != password:
            raise ValueError(partner_errmsg.get(codes.WRONG_USER_NAME_OR_PASSWORD))
        token = str(uuid.uuid4())
        # 用户信息
        user = UserListSchema.serialize(user_info)
        result = user
        result['token'] = token

        br.set(TEST_USER_INFO.format(token), result, CACHE_DAY)
        logger.info('用户 [{}] 登录了系统'.format(user_info.username))
        return result

    @staticmethod
    def logout():
        """
        登出
        :return:
        """
        token = request.headers.get('token')
        try:
            br.delete(TEST_USER_INFO.format(token))
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    def user_register(**kwargs: Any) -> "User":
        """用户注册"""
        try:
            user_data = UserSchema(**kwargs)
            user_info = User.get_user_by_name(user_data.username)
            if user_info:
                raise ValueError(partner_errmsg.get(codes.USERNAME_OR_EMAIL_IS_REGISTER))
            user = User.update(**user_data.dict())
            return user
        except Exception as err:
            logger.error(traceback.format_exc())
            raise ValueError(err)

    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        """
        获取用户列表
        :param kwargs:  查询参数
        :return:
        """
        query_data = UserQuery(**kwargs).dict()
        data = parse_pagination(User.get_all_user(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': UserListSchema.serialize(_result)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "User":
        """
        用户保存方法
        :param kwargs: 用户字段
        :return:
        """
        param = UserSchema(**kwargs)
        user = User.get(param.id) if param.id else User()
        if not user.id:
            if User.get_user_by_name(kwargs.get('username')):
                raise ValueError('用户名以存在！')
            user = User()
        # param.password = encrypt_rsa_password('Aa123456')
        # if param.roles:
        #     param.roles = ','.join(list(map(str, param.roles)))
        user_info = param.dict()
        user.update(**user_info)
        token = request.headers.get("token")
        if 'roles' in user_info:
            user_info['roles'] = list(map(int, user_info['roles'].split(",")))
        if 'tags' in user_info:
            user_info['tags'] = user_info['tags'].split(",")
        br.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)
        return user_info

    @staticmethod
    def deleted(id: Union[str, int]):
        """
        删除用户
        :param kwargs:
        :return:
        """
        try:
            user = User.get(id)
            user.delete() if user else ...
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    def check_token(token: str) -> Dict[Text, Any]:
        """
        校验token
        :param token: token
        :return:
        """
        user_info = br.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise ValueError(partner_errmsg.get(codes.PARTNER_CODE_TOKEN_EXPIRED_FAIL))

        user_info = {
            'id': user_info.get('id', None),
            'username': user_info.get('username', None)
        }
        return user_info

    @staticmethod
    def change_password(**kwargs: Any) -> "User":
        """修改密码"""
        user_id = kwargs.get('user_id', None)
        old_pwd = kwargs.get('old_pwd', None)
        new_pwd = kwargs.get('new_pwd', None)
        re_new_pwd = kwargs.get('re_new_pwd', None)
        if not user_id:
            raise ValueError(partner_errmsg.get(codes.USER_ID_IS_NULL))
        if new_pwd != re_new_pwd:
            raise ValueError(partner_errmsg.get(codes.PASSWORD_TWICE_IS_NOT_AGREEMENT))
        user_info = User.get(user_id)
        pwd = decrypt_rsa_password(user_info.password)
        if new_pwd == pwd:
            raise ValueError(partner_errmsg.get(codes.NEW_PWD_NO_OLD_PWD_EQUAL))
        if old_pwd != pwd:
            raise ValueError(partner_errmsg.get(codes.OLD_PASSWORD_ERROR))
        new_pwd = encrypt_rsa_password(new_pwd)
        user_info.password = new_pwd
        user_info.save()
        return user_info

    @staticmethod
    def get_user_info_by_token(token: str) -> Dict[Text, Any]:
        """根据token获取用户信息"""
        if not token:
            return
        user_info = br.get(TEST_USER_INFO.format(token))
        return user_info

    @staticmethod
    def get_menu_by_token():
        # 菜单权限
        user = UserService.get_user_info_by_token(request.headers.get("token", None))
        if not user:
            return []
        user_info = User.get(user.get("id"))
        if not user_info:
            return []
        roles = Roles.get_roles_by_ids(user_info.roles.split(","))
        menu_ids = []
        if roles:
            for i in roles:
                menu_ids += list(map(int, i.menus.split(',')))
        # 前端角色报错只保存子节点数据，所有这里要做处理，把父级菜单也返回给前端
        parent_ids = Menu.get_parent_id_by_ids(set(menu_ids))
        menu_ids += [i.parent_id for i in parent_ids]
        all_menu = jsonable_encoder(Menu.get_menu_by_ids(set(menu_ids)).all())
        parent_menu = [menu for menu in all_menu if menu['parent_id'] == 0]
        return MenuService.menu_assembly(parent_menu, all_menu) if menu_ids else []
