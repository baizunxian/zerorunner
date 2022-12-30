from marshmallow import Schema, fields, EXCLUDE
from typing import Optional, Text, List, Union, Any, Dict
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema
from pydantic import BaseModel


class FuncQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[Text, int]]]
    project_name: Optional[Text]
    name: Optional[Text]
    common: Optional[Text]


class FuncListSchema(BaseListSchema):
    """自定义函数"""
    project_id: Optional[int]
    name: Optional[Text]
    content: Optional[Text]


class FuncSaveOrUpdateSchema(BaseModel):
    id: Optional[int]
    content: Optional[Text]
    project_id: Optional[Text]
    name: Optional[Text]
    remarks: Optional[Text]


class FuncDebugSchema(BaseModel):
    id: Optional[int]
    func_parse_str: Optional[Text]
    func_name: Optional[Text]
    args_info: Optional[Dict[Text, Any]]
