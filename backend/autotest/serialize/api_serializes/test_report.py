import datetime
import time
from typing import Optional, Text, List, Dict, Any, Union
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
    start_time: Optional[float]
    duration: Optional[Text]
    case_id: Optional[Union[Text, int]]
    run_mode: Optional[Text]
    run_type: Optional[int]
    success: Optional[bool]
    run_count: Optional[int]
    actual_run_count: Optional[int]
    run_success_count: Optional[int]
    run_fail_count: Optional[int]
    run_skip_count: Optional[int]
    run_err_count: Optional[int]
    run_log: Optional[Text]
    project_id: Optional[int]
    module_id: Optional[int]
    env_id: Optional[int]

    @root_validator
    def root_validator(cls, data):
        if 'start_time' in data:
            data['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['start_time'])) if data[
                'start_time'] else None
        return data


class TestReportMakeSchema(BaseModel):
    """测试报告处理"""

    details: Optional[List[Dict[Text, Any]]]
    platform: Optional[Dict[Text, Any]]
    stat: Optional[Dict[Text, Any]]
    time: Optional[Dict[Text, Any]]
    success: Optional[bool]
