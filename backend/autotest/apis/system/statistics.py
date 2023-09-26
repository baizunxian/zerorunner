# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.services.system.statistic import StatisticService

router = APIRouter()


@router.post("/personalStatistics", description="个人统计")
async def personal_statistics():
    data = await StatisticService.personal_statistics()
    return partner_success(data)
