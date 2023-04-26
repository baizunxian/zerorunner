# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.corelibs.http_response import partner_success
from zerorunner.snowflake import id_center

router = APIRouter()


@router.get('/getId')
def get_all_lookup():
    """
    获取id
    :return:
    """
    data = id_center.get_id()
    return partner_success(str(data))
