# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel, validator


class BaseSchema(BaseModel):
    def dict(self, *args, **kwargs):
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return super(BaseSchema, self).dict(*args, **kwargs)

    @validator('*', pre=True)
    def blank_strings(cls, v):
        if v == "":
            return None
        return v
