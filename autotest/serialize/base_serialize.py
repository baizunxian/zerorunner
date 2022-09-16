from types import GeneratorType
from typing import Optional, Text, Any, Type, Dict, Union, Set

from pydantic import BaseModel, validator

from autotest.utils.api import jsonable_encoder

SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]


class BaseQuerySchema(BaseModel):
    def dict(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return super(BaseQuerySchema, self).dict(*args, **kwargs)

    @validator('*', pre=True)
    def blank_strings(cls, v):
        if v == "":
            return None
        return v


class BaseListSchema(BaseModel):
    id: Optional[int]
    enabled_flag: Optional[int]
    created_by: Optional[int]
    updated_by: Optional[int]
    created_by_name: Optional[Text]
    updated_by_name: Optional[Text]
    creation_date: Optional[Text]
    updation_date: Optional[Text]

    class Config:
        orm_mode = True

    @classmethod
    def serialize(cls: [Type[BaseModel]], obj: Any):
        if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
            return [cls(**jsonable_encoder(o)).dict() for o in obj]
        return cls(**jsonable_encoder(obj)).dict()

    def dict(self, *args: Any, **kwargs: Any):
        kwargs["exclude_none"] = True
        return super(BaseListSchema, self).dict(*args, **kwargs)
