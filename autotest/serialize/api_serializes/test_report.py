import json
import time

from marshmallow import Schema, EXCLUDE, fields, post_dump, post_load

from autotest.serialize.base_serialize import BaseListSchema


class TestReportQuerySchema(Schema):
    """测试报告查询"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(allow_none=True)
    ids = fields.List(fields.Int(allow_none=True), allow_none=True)
    project_name = fields.Str(allow_none=True)
    execute_user_name = fields.Str(allow_none=True)
    min_and_max = fields.Str(allow_none=True)
    report_type = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)


class TestReportSaveSchema(Schema):
    """测试报告保持"""

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(allow_none=True)
    name = fields.Str()
    start_at = fields.Float()
    scene_num = fields.Int(allow_none=True)
    duration = fields.Str(allow_none=True)
    run_type = fields.Str(allow_none=True)
    run_mode = fields.Int(allow_none=True)
    task_type = fields.Str(allow_none=True)
    project_id = fields.Int(allow_none=True)
    module_id = fields.Int(allow_none=True)
    test_count = fields.Int(allow_none=True)
    report_type = fields.Str(allow_none=True)
    run_case_priority = fields.Int(allow_none=True)
    execute_service = fields.Str(allow_none=True)
    execute_source = fields.Str(allow_none=True)
    execute_user_id = fields.Int(allow_none=True)
    execute_user = fields.Str(allow_none=True)
    execute_user_name = fields.Str(allow_none=True)
    successful_use_case = fields.Int(allow_none=True)
    run_test_count = fields.Int(allow_none=True)
    success = fields.Bool(allow_none=True)
    report_body = fields.Str()

    @post_load
    def post_load(self, data, **kwargs):
        if 'start_at' in data:
            data['start_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['start_at'])) if data[
                'start_at'] else None
        return data


class TestReportMakeSchema(Schema):
    """测试报告处理"""

    class Meta:
        unknown = EXCLUDE

    details = fields.List(fields.Dict)
    platform = fields.Dict()
    stat = fields.Dict()
    time = fields.Dict()
    success = fields.Bool()


class ReportsListSchema(BaseListSchema):
    """报告列表"""
    id = fields.Int()
    name = fields.Str()
    scene_num = fields.Int()
    duration = fields.Str()
    run_type = fields.Str()
    run_mode = fields.Int()
    task_type = fields.Str()
    project_id = fields.Int()
    module_id = fields.Int()
    test_count = fields.Int()
    report_type = fields.Str()
    run_case_priority = fields.Int()
    execute_service = fields.Str()
    execute_source = fields.Str()
    execute_user_id = fields.Int()
    execute_user = fields.Str()
    execute_user_name = fields.Str()
    successful_use_case = fields.Int()
    run_test_count = fields.Int()
    success = fields.Boolean()
    start_at = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))

    # @post_dump
    # def post_dump(self, data, **kwargs):
    #     data['report_body'] = json.loads(data['report_body'])
    #     return data

    # @staticmethod
    # def test():
    #     for i in [1]:
    #         i['execute_user_name'] = '系统' if i['execute_user_id'] == -1 else i['execute_user_name']


class ReportsLInfoSchema(BaseListSchema):
    """报告详情"""
    id = fields.Int()
    name = fields.Str()
    scene_num = fields.Int()
    duration = fields.Str()
    run_type = fields.Str()
    task_type = fields.Str()
    project_id = fields.Int()
    module_id = fields.Int()
    test_count = fields.Int()
    report_type = fields.Str()
    run_case_priority = fields.Int()
    execute_service = fields.Str()
    execute_source = fields.Str()
    execute_user_id = fields.Int()
    execute_user = fields.Str()
    execute_user_name = fields.Str()
    successful_use_case = fields.Int()
    run_test_count = fields.Int()
    success = fields.Boolean()
    report_body = fields.Str()
    start_at = fields.DateTime(format('%Y-%m-%d %H:%M:%S'))

    @post_dump
    def post_dump(self, data, **kwargs):
        data['report_body'] = json.loads(data['report_body'])
        return data
