from typing import Optional, Text, List
from pydantic import root_validator, BaseModel

from autotest.exc.exceptions import ParameterError
from autotest.models.api_models import TestSuite
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class TestSuitesQuerySchema(BaseQuerySchema):
    """测试套件查询"""

    id: Optional[int]
    ids: Optional[List[int]]
    name: Optional[Text]
    module_name: Optional[Text]
    project_name: Optional[Text]
    order_field: Optional[Text]
    created_by: Optional[int]
    created_by_name: Optional[Text]


class TestSuitesListSchema(BaseListSchema):
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


class TestSuitesSaveOrUpdateSchema(BaseModel):
    id: Optional[int]
    name: Optional[Text]
    suite_type: Optional[Text]
    project_id: Optional[int]
    include: Optional[List[int]]
    remarks: Optional[Text]
    config_id: Optional[int]

    @root_validator
    def root_validator(cls, data):
        s_id = data.get('id', None)
        s_name = data.get('name', None)
        if 'include' in data:
            data['include'] = ','.join(list(map(str, data['include']))) if data['include'] else ''

        # 判断用例名是否重复
        if s_id:
            test_suite = TestSuite.get(s_id)
            # if not test_suite:
            #     raise ValueError("用例不存在!")
            if test_suite.name != s_name:
                if TestSuite.get_list(name=s_name).first():
                    raise ParameterError("套件名以存在!")
        return data
