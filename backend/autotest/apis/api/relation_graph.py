# -*- coding: utf-8 -*-
# @author: xiao bai
from fastapi import APIRouter

from autotest.schemas.api.relation_graph import RelationGraphService, RelationIn
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post('/getRelationGraph', description="关系图")
async def api_case_list(params: RelationIn):
    data = await RelationGraphService.get_relation(params)
    return partner_success(data)
