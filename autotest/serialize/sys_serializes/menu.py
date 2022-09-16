from typing import Optional, Text

from autotest.serialize.base_serialize import BaseListSchema


class MenuListSchema(BaseListSchema):
    """菜单序列化"""
    path: Optional[Text]
    component: Optional[Text]
    title: Optional[Text]
    name: Optional[Text]
    isLink: Optional[bool]
    isHide: Optional[bool]
    isKeepAlive: Optional[bool]
    isAffix: Optional[bool]
    isIframe: Optional[bool]
    roles: Optional[Text]
    icon: Optional[Text]
    parent_id: Optional[int]
    redirect: Optional[Text]
    sort: Optional[int]
    menu_type: Optional[int]
    lookup_id: Optional[int]
    active_menu: Optional[Text]
