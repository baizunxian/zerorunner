# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import json

from zerorunner.models import TConfig, TCaseController, TestCase, WaitController, SqlController, ScriptController
from zerorunner.runner import ZeroRunner

config = TConfig(name="test")

request_dict = {
    "method": "POST",
    "url": "https://www.xiaobaicodes.com/api/blog/category_list",
    "headers": {
        "Content-Type": "application/json"
    },
    "data": {"page": 1, "pageSize": 20, "name": "$test", "time": "${get_timestamp()}"},
    "cookies": {},
    "timeout": 120,
    "allow_redirects": True,
    "verify": False,
    "upload": {}  # used for upload files
}

step_dict = {
    "name": "test",
    "case_id": '',
    "request": request_dict,
    "testcase": None,
    "variables": {"test": "测试"},
    # parameters 加入步骤 参数
    "parameters": {},
    "setup_hooks": [],
    "teardown_hooks": [],
    "message": '',
    # used to extract ,request's response field
    "extract": [],
    # used to export session variables from referenced testcase
    "export": [],
    "validators": [],
    "validate_script": [],
    "script_codes": ["""
zero.headers.set("aaa", "test1")
zero.headers.set("test", "test3")
"""],
}

# name: Text = ""
# value: Union[Text, int] = ""
# step_type: Text = ""
# enable: bool = False  # 是否有效

step_info = TCaseController(**step_dict)
wait_info = WaitController(**dict(name="test", value=1, setp_type="wait", enable=True))

sql_info = SqlController(**dict(name="sql",
                                value="select username from zero_autotest.user limit 1",
                                variable_name="username",
                                host="xiaobaicodes.com",
                                user="zero_autotest",
                                password="Bai.123456",
                                port=3306,
                                ))

script_info = ScriptController(**dict(name="脚本",
                                      value="""
zero.headers.set("aaa", "test1")
zero.headers.set("test3", "test3")
zero.headers.set("test4", "${username}")
def get_header():
    return "123456789"
zero.headers.set("test5", get_header())
""",
                                      enable=True
                                      ))
step_info.request.data = json.dumps(step_info.request.data)

step_info.setup_hooks.append(script_info)
step_info.setup_hooks.append(sql_info)

teststep_list = []
teststep_list.append(step_info)
teststep_list.append(wait_info)
teststep_list.append(sql_info)
teststep_list.append(script_info)
testcase = TestCase(config=config, teststeps=teststep_list)

zr = ZeroRunner()
zr.run_testcase(testcase)
a = zr.get_summary()
print(a)
