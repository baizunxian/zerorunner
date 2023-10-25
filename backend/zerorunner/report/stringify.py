import json
import typing
from base64 import b64encode

from zerorunner.models.result_model import RequestData, ResponseData, StepResult, TestCaseSummary

try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable
from json import JSONDecodeError
from jinja2 import escape
from requests.cookies import RequestsCookieJar


def dumps_json(value):
    """dumps json value to indented string

    Args:
        value (dict): raw json data

    Returns:
        str: indented json dump string

    """
    return json.dumps(value, indent=2, ensure_ascii=False)


def detect_encoding(value):
    try:
        return json.detect_encoding(value)
    except AttributeError:
        return "utf-8"


def __default_serialize(obj: typing.Any):
    if isinstance(obj, list):
        return [__default_serialize(o) for o in obj]
    if isinstance(obj, dict):
        return {key: __default_serialize(value) for key, value in obj.items()}

    elif isinstance(obj, bytes):
        return repr(obj)

    elif isinstance(obj, RequestsCookieJar):
        return obj.get_dict()

    elif obj is None:
        return None

    elif not isinstance(obj, (str, bytes, int, float, Iterable,)):
        # class instance, e.g. MultipartEncoder()
        return repr(obj)

    return obj


def __stringify_request(request_data: RequestData):
    """stringfy HTTP request data

    Args:
        request_data (dict): HTTP request data in dict.

            {
                "url": "http://127.0.0.1:5000/api/get-token",
                "method": "POST",
                "headers": {
                    "User-Agent": "python-requests/2.20.0",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept": "*/*",
                    "Connection": "keep-alive",
                    "user_agent": "iOS/10.3",
                    "device_sn": "TESTCASE_CREATE_XXX",
                    "os_platform": "ios",
                    "app_version": "2.8.6",
                    "Content-Type": "application/json",
                    "Content-Length": "52"
                },
                "body": b'{"sign": "cb9d60acd09080ea66c8e63a1c78c6459ea00168"}',
                "verify": false
            }

    """
    for key, value in request_data.dict().items():

        # if isinstance(value, (list, dict)):
        #     value = dumps_json(value)

        if isinstance(value, bytes):
            try:
                encoding = detect_encoding(value)
                value = value.decode(encoding)
                if key == "body":
                    try:
                        # request body is in json format
                        value = json.loads(value)
                        value = dumps_json(value)
                    except JSONDecodeError:
                        pass
                value = escape(value)
            except UnicodeDecodeError:
                pass
        elif value is None:
            pass
        else:
            value = __default_serialize(value)

        setattr(request_data, key, value)


def __stringify_response(response_data: ResponseData):
    """stringfy HTTP response data

    Args:
        response_data (dict):

            {
                "status_code": 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Content-Length": "30",
                    "Server": "Werkzeug/0.14.1 Python/3.7.0",
                    "Date": "Tue, 27 Nov 2018 06:19:27 GMT"
                },
                "encoding": "None",
                "content_type": "application/json",
                "ok": false,
                "url": "http://127.0.0.1:5000/api/users/9001",
                "reason": "NOT FOUND",
                "cookies": {},
                "body": {
                    "success": false,
                    "data": {}
                }
            }

    """
    for key, value in response_data.dict().items():

        # if isinstance(value, (list, dict)):
        #     value = dumps_json(value)

        if isinstance(value, bytes):
            try:
                encoding = response_data.encoding
                if not encoding or encoding == "None":
                    encoding = detect_encoding(value)
                    setattr(response_data, "encoding", encoding)

                if key == "body" and "image" in response_data.content_type:
                    # display image
                    value = "data:{};base64,{}".format(
                        response_data.content_type, b64encode(value).decode(encoding)
                    )
                else:
                    value = escape(value.decode(encoding))
            except UnicodeDecodeError:
                pass

        else:
            value = __default_serialize(value)

        setattr(response_data, key, value)


def __stringify_step_data(step_data: StepResult):
    if step_data.session_data and hasattr(step_data.session_data, "req_resp"):
        __stringify_request(step_data.session_data.req_resp.request)
        __stringify_response(step_data.session_data.req_resp.response)


def stringify_summary(summary: TestCaseSummary):
    """序列化 报告"""
    for index, step_data in enumerate(summary.step_results):

        if not step_data.name:
            step_data.name = "testcase {}".format(index)
        if "response" in step_data.variables:
            step_data.variables["response"] = repr(step_data.variables["response"])
        __stringify_step_data(step_data)
        step_data.variables = __default_serialize(step_data.variables)
        step_data.case_variables = __default_serialize(step_data.case_variables)
        step_data.env_variables = __default_serialize(step_data.env_variables)
        step_data.export_vars = __default_serialize(step_data.export_vars)
