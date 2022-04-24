from marshmallow import Schema, fields, EXCLUDE, post_load, post_dump

from autotest.models.api_models import TestSuite
from autotest.serialize.base_serialize import BaseListSchema


class TestSuitesQuerySchema(Schema):
    """测试套件查询"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    ids = fields.List(fields.Int(allow_none=True), allow_none=True)
    name = fields.Str(allow_none=True)
    module_name = fields.Str(allow_none=True)
    project_name = fields.Str(allow_none=True)
    order_field = fields.Str(allow_none=True)
    created_by = fields.Int(allow_none=True)
    created_by_name = fields.Str(allow_none=True)


class TestSuitesListSchema(BaseListSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    name = fields.Str()
    project_name = fields.Str()
    project_id = fields.Int()
    include = fields.Str()
    remarks = fields.Str()
    config_id = fields.Int()
    run_status = fields.Str()

    @post_dump
    def post_dump(self, data, **kwargs):
        if 'include' in data:
            data['include'] = list(map(int, data['include'].split(','))) if data['include'] else []
        return data


class TestSuitesSaveOrUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    name = fields.Str()
    suite_type = fields.Str()
    project_id = fields.Int()
    include = fields.List(fields.Int())
    remarks = fields.Str()
    config_id = fields.Int(allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
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
                    raise ValueError("套件名以存在!")
        return data
