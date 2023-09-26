# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.utils.snowflake import IDCenter

router = APIRouter()


@router.get('/getId')
def get_id():
    """
    获取id
    :return:
    """
    data = IDCenter.get_id()
    return partner_success(str(data))
