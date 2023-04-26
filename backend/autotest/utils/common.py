# -*- coding: utf-8 -*-
# @author: xiaobai
import uuid


def get_str_uuid():
    return str(uuid.uuid4()).replace("-", "")
