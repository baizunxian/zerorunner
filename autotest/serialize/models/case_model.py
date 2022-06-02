from typing import Text, Union, List, Dict

from pydantic import BaseModel, Field

text = ''


class TField(BaseModel):
    key: Text = text
    value: Text = text
    remarks_: Text = text


class Request(BaseModel):
    mode: Text = text
    language: Text = text
    data: Union[Text] = text
    form_data: List["FormData"] = []
    method: Text = text
    headers: Dict[Text, Text] = {}
    url: Text = text


class FormData(BaseModel):
    key: Text = text
    value: Union[Text, "TFileField"] = text
    type: Text = text


class TFileField(BaseModel):
    abspath: Text = text
    name: Text = text


class Variables(TField):
    type: Text = text


class Validate(BaseModel):
    check: Text = text
    comparator: Text = text
    expected: Text = text
    type: Text = text


class CaseInfo(BaseModel):
    case_id: Union[int, None] = None
    name: Text = text
    request: Request = {}
    parameters: List[TField] = []
    variables: List[Variables] = []
    setup_hooks: List[Text] = []
    teardown_hooks: List[Text] = []
    extract: List[Dict[Text, Text]] = []
    validate_script: List[Validate] = Field([], alias="validate")
