from typing import Optional, Text, List, Dict, Any

from pydantic import root_validator, BaseModel

from autotest.exc.exceptions import ParameterError
from autotest.models.api_models import ApiSuite
from autotest.serialize.api_serializes.api_case import ApiCaseBaseSchema
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class ApiSuitesQuerySchema(BaseQuerySchema):
    """测试套件查询"""

    id: Optional[int]
    ids: Optional[List[int]]
    name: Optional[Text]
    module_name: Optional[Text]
    project_name: Optional[Text]
    order_field: Optional[Text]
    created_by: Optional[int]
    created_by_name: Optional[Text]


class ApiSuitesListSchema(BaseListSchema):
    name: Optional[Text]
    project_name: Optional[Text]
    project_id: Optional[int]
    include: Optional[Text]
    remarks: Optional[Text]
    config_id: Optional[int]
    run_status: Optional[Text]

    @root_validator
    def root_validator(cls, data):
        if 'include' in data:
            data['include'] = list(map(int, data['include'].split(','))) if data['include'] else []
        return data


class ApiSuitesSchema(BaseModel):
    id: Optional[int]
    name: Optional[Text]
    env_id: Optional[Text]
    project_id: Optional[int]
    remarks: Optional[Text]
    step_data: Optional[List[Any]]
    headers: Optional[List[ApiCaseBaseSchema]]
    variables: Optional[List[ApiCaseBaseSchema]]

    @root_validator
    def root_validator(cls, data):
        s_id = data.get('id', None)
        s_name = data.get('name', None)

        # 判断用例名是否重复
        if s_id:
            test_suite = ApiSuite.get(s_id)
            if test_suite.name != s_name:
                if ApiSuite.get_list(name=s_name).first():
                    raise ParameterError("套件名以存在!")
        else:
            if ApiSuite.get_list(name=s_name).first():
                raise ParameterError("套件名以存在!")
        return data
