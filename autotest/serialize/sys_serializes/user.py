from typing import Optional, Union, Text, List

from pydantic import root_validator, BaseModel

from autotest.serialize.base_serialize import BaseListSchema, BaseQuerySchema


class UserQuery(BaseQuerySchema):
    """查询序列化"""

    id: Optional[int]
    user_ids: Optional[List[Union[int, Text]]]
    username: Optional[Text]
    nickname: Optional[Text]


class UserListSchema(BaseListSchema):
    """用户"""

    username: Optional[Text]
    email: Optional[Text]
    roles: Optional[Text]
    status: Optional[int]
    nickname: Optional[Text]
    user_type: Optional[int]
    remarks: Optional[Text]

    @root_validator
    def root_validator(cls, data):
        """"""
        if 'roles' in data and isinstance(data['roles'], str):
            data['roles'] = list(map(int, (data['roles'].split(',')))) if data['roles'] else []
        return data


class UserRegisterSchema(BaseModel):
    username: Optional[Text]
    password: Optional[Text]
    email: Optional[Text]
    link: Optional[Text]
