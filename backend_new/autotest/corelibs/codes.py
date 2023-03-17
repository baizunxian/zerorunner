# -*- coding: utf-8 -*-
# @author: xiaobai


from enum import Enum


class CodeEnum(Enum):

    @property
    def code(self):
        """获取状态吗"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]

    # 业务状态码
    PARTNER_CODE_OK = (0, "OK")
    PARTNER_CODE_FAIL = (-1, "操作失败")

    # 10000 - 11000 账号体系
    WRONG_USER_NAME_OR_PASSWORD = (10001, "账号或者密码错误！😱")  # 账号或密码错误
    PARTNER_CODE_EMPLOYEE_FAIL = (10002, "账号错误！")  # 账号错误
    WRONG_USER_NAME_OR_PASSWORD_LOCK = (10003, "密码输入错误超过次数，请5分钟后再登录！😭")
    USERNAME_OR_EMAIL_IS_REGISTER = (10004, "用户名已被注册")
    USER_ID_IS_NULL = (10005, "用户id不能为空")
    PASSWORD_TWICE_IS_NOT_AGREEMENT = (10006, "两次输入的密码不一致")
    NEW_PWD_NO_OLD_PWD_EQUAL = (10007, "新密码不能与旧密码相同")
    OLD_PASSWORD_ERROR = (10008, "旧密码错误")

    # 用户状态 验证  11000 - 12000
    PARTNER_CODE_TOKEN_EXPIRED_FAIL = (11000, "用户信息以已过期 😂")  # token已过期

    # 参数类型 12000 - 13000
    PARTNER_CODE_PARAMS_FAIL = (12000, "必填参数不能为空 😅")  # 必填参数不能为空

    # project 项目 13000 - 14000
    PROJECT_HAS_MODULE_ASSOCIATION = (13000, "项目有模块或用例关联，不能删除")
    PROJECT_NAME_EXIST = (13001, "项目名已存在")  # 项目名以存在

    # module 模块 14000 - 15000
    MODULE_HAS_CASE_ASSOCIATION = (14000, " 模块有用例关联, 请删除对于模块下的用例")  # 模块有用例关联
    MODULE_NAME_EXIST = (14001, "模块名已存在")  # 模块名以存在

    # case 用例/配置 15000 - 16000
    CASE_NAME_EXIST = (15000, "用例名已存在，请重新命名")
    SUITE_NAME_EXIST = (15001, "套件名已存在，请重新命名")
    CASE_NOT_EXIST = (15002, "用例不存在")
    CASE_UPLOAD_FROM_POSTMAN = (15003, "导入失败")

    # 菜单管理  16000 - 17000
    MENU_HAS_MODULE_ASSOCIATION = (16000, "当前菜单下管理的子菜单，不能删除！")  #
    MENU_NAME_EXIST = (16001, "菜单名称已存在")  # 菜单名以存在

    # lookup 数据字典 17000 - 18000
    LOOKUP_CODE_NOT_EMPTY = (17000, "字典code不能为空!")  # 菜单名以存在
    LOOKUP_NOT_EXIST = (17001, "字典不存在!")  # 菜单名以存在
    LOOKUP_CODE_EXIST = (17002, "字典code已存在!")  # 菜单名以存在

    # task 定时任务 18000 - 19000
    TASK_NAME_EXIST = (18000, "定时任务名称以存在")
