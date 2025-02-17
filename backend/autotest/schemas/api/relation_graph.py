# -*- coding: utf-8 -*-
# @author: xiao bai
import typing

from pydantic import BaseModel, Field
from enum import Enum

from autotest.models.api_models import ApiInfo, ApiCaseStep, ApiCase
from autotest.models.celery_beat_models import TimedTaskCase, TimedTask


class RelationTypeEnum(str, Enum):
    API = "api"
    CASE = "case"
    TIMED_TASK = "timed_task"


class RelationIn(BaseModel):
    id: typing.Union[int, str] = Field(..., description="id")
    type: str = Field(..., description="类型")


class RelationData(BaseModel):
    id: typing.Union[int, str] = Field(None, description="id")
    relation_id: str = Field(None, description="relation_id")
    from_relation_id: str = Field(None, description="from_relation_id")
    to_relation_id: str = Field(None, description="to_relation_id")
    type: str = Field(None, description="类型")
    name: str = Field(None, description="名称")
    created_by_name: str = Field(None, description="创建人")
    creation_date: str = Field(None, description="创建时间")


class RelationResult(BaseModel):
    id: typing.Union[str] = Field(None, description="关系id")
    data: RelationData = Field({}, description="关系数据")


class RelationGraphService:

    @staticmethod
    async def get_relation(params: RelationIn):
        """
        获取关系
        :param params:
        :return:
        """
        if params.type == RelationTypeEnum.API.value:
            return await RelationGraphService.api_use_relation(params)
        elif params.type == RelationTypeEnum.CASE.value:
            return await RelationGraphService.case_use_relation(params)
        elif params.type == RelationTypeEnum.TIMED_TASK.value:
            return await RelationGraphService.timed_task_use_relation(params)
        else:
            raise ValueError("类型错误！💔")

    @staticmethod
    async def api_use_relation(params: RelationIn):
        """
        api使用关系
        :param params:
        :return:
        """

        api_info = await ApiInfo.get_api_by_id(params.id)
        if not api_info:
            raise ValueError('不存在当前接口！')
        line_list = []
        node_list = []

        # api关联到的测试用例
        api_relation_id = f"api_{params.id}"
        node_list.append(RelationResult(id=api_relation_id, data=RelationData(**api_info, type='api')))
        api_case_relation_data = await ApiCaseStep.get_relation_by_api_id(params.id) or []

        node_, line_, case_set = await RelationGraphService.handler_relation_data(api_case_relation_data,
                                                                                  RelationTypeEnum.CASE)
        node_list.extend(node_)
        line_list.extend(line_)

        # case - timed task 关联
        timed_task_relation_data = await TimedTaskCase.get_relation_by_case_ids(list(case_set)) or []

        node_, line_, timed_task_set = await RelationGraphService.handler_relation_data(timed_task_relation_data,
                                                                                        RelationTypeEnum.TIMED_TASK)
        node_list.extend(node_)
        line_list.extend(line_)

        data = {
            "rootId": api_relation_id,
            "nodes": node_list,
            "lines": line_list,
            "api_count": 0,
            "case_count": len(case_set),
            "timed_task_count": len(timed_task_set)
        }
        return data

    @staticmethod
    async def case_use_relation(params: RelationIn):
        """
        用例使用关系
        :param params:
        :return:
        """
        api_info = await ApiCase.get_api_by_id(params.id)
        if not api_info:
            raise ValueError('不存在当前用例！')

        line_list = []
        node_list = []

        # case - api关联到的测试用例
        case_relation_id = f"case_{params.id}"
        node_list.append(RelationResult(id=case_relation_id, data=RelationData(**api_info, type='case')))

        api_relation_data = await ApiCaseStep.get_relation_by_case_ids([params.id]) or []
        node_, line_, api_set = await RelationGraphService.handler_relation_data(api_relation_data,
                                                                                 RelationTypeEnum.API)
        node_list.extend(node_)
        line_list.extend(line_)

        # case - timed task 关联
        timed_task_relation_data = await TimedTaskCase.get_relation_by_case_ids([params.id]) or []
        node_, line_, timed_task_set = await RelationGraphService.handler_relation_data(timed_task_relation_data,
                                                                                        RelationTypeEnum.TIMED_TASK)
        node_list.extend(node_)
        line_list.extend(line_)
        data = {
            "rootId": case_relation_id,
            "nodes": node_list,
            "lines": line_list,
            "api_count": len(api_set),
            "case_count": 0,
            "timed_task_count": len(timed_task_set)
        }
        return data

    @staticmethod
    async def timed_task_use_relation(params: RelationIn):
        """
        定时任务使用关系
        :param params:
        :return:
        """
        timed_task = await TimedTask.get_timed_task_by_id(params.id)
        if not timed_task:
            raise ValueError('不存在当前定时任务！')

        line_list = []
        node_list = []
        timed_task_relation_id = f"timed_task_{params.id}"
        node_list.append(RelationResult(id=timed_task_relation_id, data=RelationData(**timed_task, type='timed_task')))
        case_relation_data = await TimedTaskCase.get_relation_by_timed_task_ids([params.id]) or []
        node_, line_, case_set = await RelationGraphService.handler_relation_data(case_relation_data,
                                                                                  RelationTypeEnum.CASE)
        node_list.extend(node_)
        line_list.extend(line_)

        api_relation_data = await ApiCaseStep.get_relation_by_case_ids(list(case_set)) or []
        node_, line_, api_set = await RelationGraphService.handler_relation_data(api_relation_data,
                                                                                 RelationTypeEnum.API)
        node_list.extend(node_)
        line_list.extend(line_)

        data = {
            "rootId": timed_task_relation_id,
            "nodes": node_list,
            "lines": line_list,
            "api_count": len(api_set),
            "case_count": len(case_set),
            "timed_task_count": 0
        }
        return data

    @staticmethod
    async def handler_relation_data(relation_data: typing.List, relation_type: RelationTypeEnum):
        """"""
        node_list = []
        line_list = []
        relation_set = set()

        for relation in relation_data:
            relation = RelationData.parse_obj(relation)
            relation.type = relation_type.value
            node_list.append(RelationResult(id=relation.relation_id, data=relation))
            line_list.append({
                "from": relation.from_relation_id,
                "to": relation.to_relation_id,
                "text": f"关联{relation_type.value}"
            })
            relation_set.add(relation.id)

        return node_list, line_list, relation_set
