import json

from marshmallow import Schema, EXCLUDE, fields, post_load, post_dump

from autotest.models.api_models import CaseInfo
from autotest.serialize.base_serialize import BaseListSchema
from autotest.utils.service_utils import check_testcase


class CaseQuerySchema(Schema):
    """查询参数序列化"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Str() or fields.Int())
    name = fields.Str()
    case_status = fields.Int()
    case_type = fields.Int()
    code = fields.Str()
    sort_type = fields.Str()
    priority = fields.Int()
    project_id = fields.Int()
    module_id = fields.Int()
    module_ids = fields.List(fields.Int())
    project_name = fields.Str()
    order_field = fields.Str()
    created_by = fields.Int()
    created_by_name = fields.Str()


class CaseSaveOrUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    """用例保存更新"""
    id = fields.Int(allow_none=True)
    name = fields.Str(required=True)
    user_id = fields.Int()
    case_status = fields.Int()
    case_type = fields.Int()
    code = fields.Str(required=False)
    include = fields.List(fields.Int(), allow_none=True)
    testcase = fields.Dict()
    code_id = fields.Int(allow_none=True)
    priority = fields.Int(allow_none=True, required=False)
    config_id = fields.Int(allow_none=True, required=False)
    project_id = fields.Int(allow_none=True)
    module_id = fields.Int(allow_none=True)
    created_by = fields.Int()

    @post_load
    def post_load(self, data, **kwargs):
        id = data.get("id", None)
        name = data.get("name", None)
        if not data.get("name"):
            raise ValueError("用例名不能为空!")
        # 判断用例名是否重复
        if id:
            case_info = CaseInfo.get(id)
            if not case_info:
                raise ValueError("用例不存在!")
            if case_info.name != name:
                if CaseInfo.get_case_by_name(name=name):
                    raise ValueError("用例名重复!")

        if 'include' in data:
            data["include"] = ",".join(str(i) for i in data["include"]) if data["include"] else ""
        if data.get("testcase"):
            check_testcase(**data["testcase"])
            data["testcase"] = json.dumps(data["testcase"])  # 将字典转换为json字符串
        return data


class CaseInfoListSchema(BaseListSchema):
    """
    用例详情
    """
    id = fields.Int()
    name = fields.Str()
    type = fields.Int()
    service_name = fields.Str()
    project_id = fields.Int()
    project_name = fields.Str()
    module_id = fields.Int()
    module_name = fields.Str()
    include = fields.Str()
    testcase = fields.Str()
    run_type = fields.Int()
    code_id = fields.Str()
    code = fields.Str()
    config_id = fields.Int()
    priority = fields.Int()
    run_status = fields.Str()

    @post_dump
    def post_dump(self, data, **kwargs):
        if 'include' in data:
            data["include"] = list(map(int, data["include"].split(","))) if data["include"] else []
        if data.get("testcase"):
            data["testcase"] = json.loads(data["testcase"])
        return data


class TestCaseRunBodySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    """"""
    id = fields.Int()
    name = fields.Str()
    # user_id = fields.Int()
    case_status = fields.Int()
    case_type = fields.Int()
    code = fields.Str(allow_none=True)
    run_type = fields.Int()
    include = fields.Str()
    testcase = fields.Str()
    code_id = fields.Int(allow_none=True)
    priority = fields.Int(allow_none=True)
    config_id = fields.Int(allow_none=True)
    project_id = fields.Int(allow_none=True)
    module_id = fields.Int(allow_none=True)
    created_by = fields.Int()

    @post_dump
    def post_dump(self, data, **kwargs):
        if data['testcase']:
            data['testcase'] = json.loads(data['testcase'])
        if 'include' in data:
            data["include"] = list(map(int, data["include"].split(","))) if data["include"] else []
        return data


class TestCaseRunSchema(Schema):
    """运行用例"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    ids = fields.List(fields.Int(allow_none=True), allow_none=True)
    base_url = fields.Str()
    name = fields.Str()
    run_type = fields.Str()
    run_mode = fields.Int()
    testcase_dir_path = fields.Str(allow_none=True)

    # created_by_name = fields.Str(allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        if not data.get("base_url"):
            data['base_url'] = ""
        if not data.get("id"):
            raise ValueError("请选择用例!")
        return data


class TestCaseRunBatchSchema(Schema):
    """批量运行用例"""

    class Meta:
        unknown = EXCLUDE

    ids = fields.List(fields.Str())
    base_url = fields.Str()
    name = fields.Str()
    project_id = fields.Int()
    run_type = fields.Str()
    run_mode = fields.Int()
    ex_user_id = fields.Int()
    testcase_dir_path = fields.Str(allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        if not data.get("base_url"):
            data['base_url'] = ""
        if 'ids' in data:
            data['ids'] = list(map(int, data.get('ids')))
        return data
