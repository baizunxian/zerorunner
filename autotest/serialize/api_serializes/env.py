from typing import Optional, Text, List, Union
from pydantic import root_validator, BaseModel
from autotest.models.api_models import Env
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class EnvQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[int, Text]]]
    name: Optional[Text]
    created_by_name: Optional[Text]


# class EnvListSchema(BaseListSchema):
#     """环境序列化"""
#     name: Optional[Text]
#     url: Optional[Text]
#     remarks: Optional[Text]


class EnvListSchema(BaseListSchema):
    """环境序列化"""
    name: Text
    url: Optional[Text]
    remarks: Optional[Text]


class EnvSaveOrUpdateSchema(BaseModel):

    id: Optional[int]
    name: Optional[Text]
    url: Optional[Text]
    remarks: Optional[Text]

    @root_validator
    def root_validator(cls, data):
        e_id = data.get('id', None)
        e_name = data.get('name', None)
        e_url = data.get('url', None)

        if not e_name:
            raise ParameterError('环境名称不能为空')
        else:
            if Env.get_list(name=e_name).first():
                raise ParameterError("环境名称已存在!")
        if not e_url:
            raise ParameterError('环境地址不能为空')

        # 判断名称是否重复
        if e_id:
            env = Env.get(e_id)
            if not env:
                raise ParameterError("数据跟新失败，环境不存在！")
            if env.name != e_name:
                if env.get_list(name=e_name).first():
                    raise ParameterError("环境名称已存在!")
        return data
