from typing import Optional, Text, List, Union

from autotest.serialize.base_serialize import BaseQuerySchema


class ModuleQuerySchema(BaseQuerySchema):
    """查询参数序列化"""

    id: Optional[int]
    ids: Optional[List[Union[int, Text]]]
    name: Optional[Text]
    project_name: Optional[Text]
    project_id: Optional[int]
    order_field: Optional[Text]
    sort_type: Optional[int]
    created_by_name: Optional[Text]
