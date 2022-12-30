# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel
from typing import Optional, Text, List


class AsyncRunCaseSchema(BaseModel):
    id: Optional[int]
    ids: Optional[List[int]]
    # task_type: int  # 10 用例 20 套件
    run_mode: Text  # case 用例 suites 套件
    run_type: Optional[Text]
    base_url: Text
