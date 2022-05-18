import json
import os
import time

import pytest
from loguru import logger

from autotest.httprunner.utils import get_platform, ExtendJSONEncoder


@pytest.fixture(scope="session", autouse=True)
def session_fixture(request):
    """setup and teardown each task"""
    start_at = time.time()

    yield

    summary = {
        "success": True,
        "stat": {
            "testcases": {"total": 0, "success": 0, "fail": 0},
            "teststeps": {"total": 0, "failures": 0, "successes": 0},
        },
        "time": {"start_at": start_at, "duration": time.time() - start_at},
        "platform": get_platform(),
        # 用例步骤详情
        "details": [],
    }

    summary_path = ''
    for item in request.node.items:
        if not summary_path:
            summary_path = item.fspath.dirname
        testcase_summary = item.instance.get_summary()
        summary["success"] &= testcase_summary.success

        summary["stat"]["testcases"]["total"] += 1
        summary["stat"]["teststeps"]["total"] += len(testcase_summary.step_datas)
        if testcase_summary.success:
            summary["stat"]["testcases"]["success"] += 1
            summary["stat"]["teststeps"]["successes"] += len(
                testcase_summary.step_datas
            )
        else:
            summary["stat"]["testcases"]["fail"] += 1
            summary["stat"]["teststeps"]["successes"] += (
                    len(testcase_summary.step_datas) - 1
            )
            summary["stat"]["teststeps"]["failures"] += 1

        testcase_summary_json = testcase_summary.dict()
        testcase_summary_json["step_datas"] = testcase_summary_json.pop("step_datas")
        summary["details"].append(testcase_summary_json)

    os.makedirs(summary_path, exist_ok=True)
    summary_path = os.path.join(summary_path, 'summary.json')

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False, cls=ExtendJSONEncoder)
