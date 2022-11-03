import json
from typing import Optional, Text, List, Union, Dict, Any
from pydantic import root_validator, BaseModel
from autotest.exc.exceptions import ParameterError
from autotest.models.api_models import CaseInfo
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema
from autotest.utils.service_utils import check_testcase


class CaseQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[int, Text]]]
    name: Optional[Text]
    case_status: Optional[int]
    case_type: Optional[int]
    code: Optional[Text]
    sort_type: Optional[Text]
    priority: Optional[int]
    project_id: Optional[int]
    module_id: Optional[int]
    module_ids: Optional[List[int]]
    project_name: Optional[Text]
    order_field: Optional[Text]
    created_by: Optional[int]
    created_by_name: Optional[Text]


class CaseSaveOrUpdateSchema(BaseModel):
    """用例保存更新"""
    id: Optional[int]
    name: Optional[Text]
    user_id: Optional[int]
    case_status: Optional[int]
    case_type: Optional[int]
    code: Optional[Text]
    include: Optional[List[Text]]
    testcase: Optional[Dict[Text, Any]]
    code_id: Optional[int]
    priority: Optional[int]
    config_id: Optional[int]
    project_id: Optional[int]
    module_id: Optional[int]
    created_by: Optional[int]

    @root_validator
    def root_validator(cls, data):
        id = data.get("id", None)
        name = data.get("name", None)
        if not data.get("name"):
            raise ParameterError("用例名不能为空!")
        # 判断用例名是否重复
        if id:
            case_info = CaseInfo.get(id)
            if not case_info:
                raise ParameterError("用例不存在!")
            if case_info.name != name:
                if CaseInfo.get_case_by_name(name=name):
                    raise ParameterError("用例名重复!")

        if 'include' in data and isinstance(data["include"], list):
            data["include"] = ",".join(data["include"])
        if data.get("testcase"):
            check_testcase(**data["testcase"])
            data["testcase"] = json.dumps(data["testcase"])  # 将字典转换为json字符串
        return data


class TestCaseRunBodySchema(BaseListSchema):
    """"""
    name: Optional[Text]
    # user_id: Optional[int]
    case_status: Optional[int]
    case_type: Optional[int]
    code: Optional[Text]
    run_type: Optional[int]
    include: Optional[Text]
    testcase: Optional[Text]
    code_id: Optional[int]
    priority: Optional[int]
    config_id: Optional[int]
    project_id: Optional[int]
    module_id: Optional[int]
    created_by: Optional[int]

    @root_validator
    def root_validator(cls, data):
        if data['testcase']:
            data['testcase'] = json.loads(data['testcase'])
        if 'include' in data:
            data["include"] = list(map(int, data["include"].split(","))) if data["include"] else []
        return data


class TestCaseRunSchema(BaseModel):
    """运行用例"""

    id: Optional[int]
    ids: Optional[List[int]]
    base_url: Optional[Text]
    name: Optional[Text]
    run_type: Optional[Text]
    run_mode: Optional[int]
    number_of_run: Optional[int]
    testcase_dir_path: Optional[Text]

    # created_by_name :Optional[Text]

    @root_validator
    def root_validator(cls, data):
        if not data.get("base_url"):
            data['base_url'] = ""
        if not data.get("id"):
            raise ParameterError("请选择用例!")
        return data


class TestCaseRunBatchSchema(BaseModel):
    """批量运行用例"""

    ids: Optional[List[Union[Text, int]]]
    base_url: Optional[Text]
    name: Optional[Text]
    project_id: Optional[int]
    run_type: Optional[Text]
    run_mode: Optional[int]
    ex_user_id: Optional[int]
    testcase_dir_path: Optional[Text]

    @root_validator(pre=True)
    def root_validator(cls, data):
        if not data.get("base_url", None):
            data['base_url'] = ""
        if 'ids' in data:
            data['ids'] = list(map(int, data.get('ids')))
        return data
