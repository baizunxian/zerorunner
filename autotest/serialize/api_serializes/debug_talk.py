from marshmallow import Schema, fields, EXCLUDE
from typing import Optional, Text, List, Union
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class DebugTalkQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[Text, int]]]
    project_name: Optional[Text]
    name: Optional[Text]
    common: Optional[Text]


class DebugTalkListSchema(BaseListSchema):
    """自定义函数"""
    project_id: Optional[int]
    project_name: Optional[Text]
    debug_talk: Optional[Text]


class DebugTalkSaveOrUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id: Optional[int]
    debug_talk: Optional[Text]
    project_id: Optional[Text]


class DebugTalkDebugSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id: Optional[int]
    func_parse_str: Optional[Text]
    func_name: Optional[Text]
    args_info = fields.Dict()
