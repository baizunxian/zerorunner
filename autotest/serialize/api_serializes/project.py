from typing import Optional, List, Text, Union

from autotest.serialize.base_serialize import BaseQuerySchema


class ProjectQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[int, Text]]]
    name: Optional[Text]
    order_field: Optional[Text]
    sort_type: Optional[int]
    created_by_name: Optional[Text]
