# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema


class MenuIn(BaseModel):
    id: int = Field(None, description='id')
    path: str = Field(..., description='路径')
    name: str = Field(..., description='组件名称')
    component: str = Field(..., description='组件路径')
    title: str = Field(..., description='路由名称')
    isLink: bool = Field(False,
                         description='是否是链接 开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    linkUrl: str = Field(None, description='链接地址')
    isHide: bool = Field(False, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive: bool = Field(True, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isAffix: bool = Field(False, description='是否固定')
    isIframe: bool = Field(False, description='是否内嵌')
    icon: str = Field("", description='菜单图标')
    parent_id: str = Field(..., description='父级菜单id')
    redirect: str = Field(None, description='重定向路由')
    sort: int = Field(0, description='排序')
    menu_type: int = Field(..., description='菜单类型')
    active_menu: str = Field(None, description='显示页签')


class MenuUpdate(MenuIn):
    pass


class MenuDel(BaseModel):
    id: int = Field(..., title="id", description='id')


class MenuViews(BaseModel):
    menu_id: int = Field(..., title="id", description='菜单id')


class Menu(BaseSchema):
    name: str = Field(None, description='组件名称')


class MenuMateSchemas(BaseSchema):
    icon: str = Field(None, description='菜单图标')
    isAffix: bool = Field(None, description='是否固定')
    isHide: bool = Field(None, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isIframe: bool = Field(None, description='是否内嵌')
    isKeepAlive: bool = Field(None, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isLink: bool = Field(None, description="url")
    roles: list = Field(None, description='角色')
    title: str = Field(None, description='路由名称')


class MenuRouterSchemas(BaseSchema):
    name: str = Field(None, description='组件名称')
    parent_id: int = Field(None, description='父级菜单id')
    path: str = Field(None, description='路径')
    redirect: str = Field(None, description='重定向路由')
    sort: int = Field(None, description='排序')
    title: str = Field(None, description='路由名称')
    active_menu: str = Field(None, description='显示页签')
    component: str = Field(None, description='组件路径')
    created_by: int = Field(None, description='创建人')
    updated_by: int = Field(None, description='更新人')
    creation_date: str = Field(None, description='创建时间')
    updation_date: str = Field(None, description='更新时间')
    enabled_flag: int = Field(None, description='是否启用')
    isLink: bool = Field(None,
                         description='是否是链接 开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    menu_type: int = Field(None, description='菜单类型')
    meta: MenuMateSchemas = Field(None, description='菜单元数据')
    views: int = Field(None, description='菜单访问量')
    trace_id: str = Field(None, description='跟踪id')
