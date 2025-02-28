# -*- coding: utf-8 -*-
# @author: xiao bai

import json
from enum import Enum
from typing import Text, List, Dict, Union
from urllib.parse import urlparse

from loguru import logger
from pydantic import BaseModel



class BodyTypeEnum(Text, Enum):
    body_raw = "raw"
    body_url_encoded = "urlencoded"
    body_form_data = "formdata"
    body_file = "file"
    body_graph_qL = "graphql"


class FieldTypeEnum(Text, Enum):
    file_type_text = "text"
    file_type_file = "file"


# 内容
content_type = {
    "text": "text/plain",
    "javascript": "application/javascript",
    "json": "application/json",
    "html": "text/html",
    "xml": "application/xml",
}

text = ''


class TField(BaseModel):
    key: Text = None
    value: Text = None
    src: Text = None
    description: Text = text
    type: Text = None
    disabled: Union[bool, None] = None
    enable: Union[bool, None] = None


class TInfo(BaseModel):
    name: Text = text
    description: Text = text
    # schema: Text


class TBody(BaseModel):
    mode: Text = text
    formdata: List[TField] = []
    urlencoded: List[TField] = []
    raw: Text = text
    disabled: Union[bool, None] = None
    options: Dict = {}


class TUrl(BaseModel):
    raw: Text = text
    protocol: Text = text
    path: List[Text] = text
    description: Text = text
    query: List[TField] = []
    variable: List[TField] = []


class TRequest(BaseModel):
    method: Text = text
    header: Union[List[TField], None] = []
    body: TBody = {}
    url: TUrl = {}
    description: Text = text


class TResponse(BaseModel):
    name: Text = text
    originalRequest: TRequest = {}
    status: Text = text
    code: int = None
    header: Union[List[TField], None] = []
    body: Text = text


class TItem(BaseModel):
    name: Text = text
    item: List['TItem'] = []
    request: TRequest = {}
    response: List[TResponse] = []


class TCollection(BaseModel):
    info: TInfo
    item: List[TItem]


class Collection:

    def __init__(self, postman_body):
        self.item_list: List[TItem] = []
        self.case_list: List[CaseInfo] = []
        self.postman_body = postman_body

    def make_test_case(self):
        t_collection = self.load()
        self.prepare_test_steps(t_collection)

    def load(self):
        collection = TCollection.parse_obj(self.postman_body)
        return collection

    def prepare_test_steps(self, t_collection: TCollection):
        for item in t_collection.item:
            print()
            self.extract_item_list(item)

        for item in self.item_list:
            case: CaseInfo = self.prepare_test_step(item)
            self.case_list.append(case)

    def extract_item_list(self, item: TItem):

        if len(item.item) == 0:
            if item.request:
                self.item_list.append(item)
        for i in item.item:
            i.name = f"{item.name} - {i.name}"
            self.extract_item_list(i)

    @staticmethod
    def prepare_test_step(item: TItem):
        logger.info(f"method: {item.request.method}, url: {item.request.url.raw}")
        test_case = TestCase()
        test_case.make_request_name(item)
        test_case.make_request_method(item)
        test_case.make_request_url(item)
        test_case.make_request_params(item)
        test_case.make_request_headers_and_cookies(item)
        test_case.make_request_body(item)
        test_case.make_validate(item)

        return test_case.case_info


class TestCase:
    def __init__(self):
        self.case_info = CaseInfo()
        self.case_request = Request()

    def make_request_name(self, item: TItem):
        self.case_info.name = item.name

    def make_request_method(self, item: TItem):
        self.case_request.method = item.request.method
        self.case_request.mode = item.request.body.mode if hasattr(item.request.body, 'mode') else ''
        self.case_request.language = item.request.body.options.get('language', '') if hasattr(item.request.body,
                                                                                              'options') else ''
        self.case_info.request = self.case_request

    def make_request_url(self, item: TItem):
        raw_url = item.request.url.raw
        for field in item.request.url.variable:
            path_var = f":{field.key}"
            raw_url = raw_url.replace(path_var, field.value, -1)
        try:
            u = urlparse(raw_url)
            self.case_info.request.url = f"{u.scheme}://{u.netloc}{u.path}"
        except Exception:
            logger.error('parse URL error')

    def make_request_params(self, item: TItem):
        pass

    def make_request_headers_and_cookies(self, item: TItem):
        self.case_info.request.headers = {}
        for field in item.request.header:
            if field.disabled:
                continue
            if field.key == 'cookie':
                # self.case_info.request.cookies[field.key] = field.value
                ...
            self.case_info.request.headers[field.key] = field.value

    def make_request_body(self, item: TItem):
        if not hasattr(item.request.body, 'mode'):
            return
        mode = item.request.body.mode
        if mode == BodyTypeEnum.body_raw:
            self.make_request_body_raw(item)

        if mode == BodyTypeEnum.body_form_data:
            self.make_request_body_form_data(item)

        if mode == BodyTypeEnum.body_url_encoded:
            self.make_request_body_url_encoded(item)

    def make_request_body_raw(self, item: TItem):
        i_options = item.request.body.options
        i_language = i_options.get('raw', None)
        language_type = i_language.get('language', None)
        raw_body = item.request.body.raw

        self.case_info.request.data = raw_body
        if language_type == 'json':
            self.case_info.request.language = 'JSON'
        elif language_type == 'text':
            self.case_info.request.language = 'Text'
        self.case_info.request.headers['Content-Type'] = content_type[language_type]

    def make_request_body_form_data(self, item: TItem):
        self.case_info.request.mode = 'form_data'
        for field in item.request.body.formdata:
            if field.disabled:
                continue
            if field.type == FieldTypeEnum.file_type_text:
                self.case_info.request.form_data.append(FormData(**field.dict()))
            elif field.type == FieldTypeEnum.file_type_file:
                write_form_data_file(field)

    def make_request_body_url_encoded(self, item: TItem):
        self.case_info.request.mode = 'data'
        pay_load = {}
        for field in item.request.body.urlencoded:
            if field.disabled:
                continue
            pay_load[field.key] = field.value
        self.case_info.request.data = pay_load
        self.case_info.request.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def make_validate(self, item: TItem):
        pass


def write_form_data_file(field: TField):
    with open(field.src, 'r') as f:
        pass


if __name__ == '__main__':
    with open('test.json', 'rb') as f:
        coll = Collection(json.load(f))
    coll.make_test_case()
    print(coll.case_list)