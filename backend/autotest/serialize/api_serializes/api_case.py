import json
from typing import Optional, Text, List, Union, Dict, Any
from pydantic import root_validator, BaseModel
from autotest.exc.exceptions import ParameterError
from autotest.models.api_models import ApiCase
from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema
from enum import Enum
from zerorunner.models import SqlController, WaitController, ScriptController, JsonPathData, TStep


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


class ApiCaseBaseSchema(BaseModel):
    key: Text = ""
    value: Text = ""
    remarks: Text = ""


class ApiCaseValidatorsSchema(BaseModel):
    mode: Text = ""
    check: Text = ""
    expect: Text = ""
    comparator: Text = ""


class ApiCaseBodySchema(BaseModel):
    mode: Text = ""
    data: Text = ""
    language: Text = ""


class ApiCaseHooksSchema(BaseModel):
    name: Text = ""
    index: Union[Text, int] = ""
    value: Union[Any] = ""
    enable: bool = ""
    step_type: Text = ""


class ExtractSchema(BaseModel):
    name: Text = ""
    path: Text = ""
    extractType: Text = ""


class StepExtractSchema(ApiCaseHooksSchema):
    value: List[ExtractSchema]


class StepScriptSchema(ApiCaseHooksSchema):
    pass


class StepSqlSchema(ApiCaseHooksSchema):
    env_id: int = None
    source_id: int = None
    variable_name: Text = ""
    timeout: int = None


class StepWaitSchema(ApiCaseHooksSchema):
    pass


class StepTypeEnum(Enum):
    sql = "sql"
    wait = "wait"
    extract = "extract"
    case = "case"
    script = "script"


class CaseSaveOrUpdateSchema(BaseModel):
    """用例保存更新"""
    id: Union[int, Text]
    name: Text = ""
    project_id: int = None
    module_id: int = None
    case_status: int = None
    code_id: int = None
    code: Text = None
    priority: int = None
    case_tag: Text = ""
    method: Text = ""
    url: Text = ""
    request_body: Union[ApiCaseBodySchema, None] = {}
    setup_hooks: Union[List[Dict[Text, Any]], None] = []
    teardown_hooks: Union[List[Dict[Text, Any]], None] = []
    variables: Union[List[ApiCaseBaseSchema], None] = []
    headers: Union[List[ApiCaseBaseSchema], None] = []
    validators: Union[List[ApiCaseValidatorsSchema], None] = []

    @root_validator
    def root_validator(cls, data):
        id = data.get("id", None)
        name = data.get("name", None)
        if not data.get("name"):
            raise ParameterError("用例名不能为空!")
        # 判断用例名是否重复
        if id:
            case_info = ApiCase.get(id)
            if not case_info:
                raise ParameterError("用例不存在!")
            if case_info.name != name:
                if ApiCase.get_case_by_name(name=name):
                    raise ParameterError("用例名重复!")

        return data


class ApiCaseSchema(BaseModel):
    name: Text = ""
    project_id: int = None
    module_id: int = None
    case_status: int = None
    code_id: int = None
    code: Text = None
    priority: int = None
    case_tag: Text = ""
    method: Text = ""
    url: Text = ""
    env_id: Union[Text, int, None] = None
    request_body: Union[ApiCaseBodySchema, None] = {}
    setup_hooks: Union[List[Dict[Text, Any]], None] = []
    teardown_hooks: Union[List[Dict[Text, Any]], None] = []
    variables: Union[List[ApiCaseBaseSchema], None] = []
    headers: Union[List[ApiCaseBaseSchema], None] = []
    validators: Union[List[ApiCaseValidatorsSchema], None] = []
