import time
from typing import Optional, Text, List, Dict, Any
from pydantic import BaseModel, root_validator
from autotest.serialize.base_serialize import BaseQuerySchema


class TestReportQuerySchema(BaseQuerySchema):
    """测试报告查询"""

    id: Optional[int]
    ids: Optional[List[int]]
    project_name: Optional[Text]
    execute_user_name: Optional[Text]
    min_and_max: Optional[Text]
    report_type: Optional[Text]
    name: Optional[Text]


class TestReportSaveSchema(BaseModel):
    """测试报告保持"""

    id: Optional[Text]
    name: Optional[Text]
    start_at: Optional[float]
    scene_num: Optional[int]
    duration: Optional[Text]
    run_type: Optional[Text]
    run_mode: Optional[int]
    task_type: Optional[Text]
    project_id: Optional[int]
    module_id: Optional[int]
    test_count: Optional[int]
    report_type: Optional[Text]
    run_case_priority: Optional[int]
    execute_service: Optional[Text]
    execute_source: Optional[Text]
    execute_user_id: Optional[int]
    execute_user: Optional[Text]
    execute_user_name: Optional[Text]
    successful_use_case: Optional[int]
    run_test_count: Optional[int]
    success: Optional[bool]
    report_body: Optional[Text]

    @root_validator
    def root_validator(cls, data):
        if 'start_at' in data:
            data['start_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['start_at'])) if data[
                'start_at'] else None
        return data


class TestReportMakeSchema(BaseModel):
    """测试报告处理"""

    details: Optional[List[Dict[Text, Any]]]
    platform: Optional[Dict[Text, Any]]
    stat: Optional[Dict[Text, Any]]
    time: Optional[Dict[Text, Any]]
    success: Optional[bool]
