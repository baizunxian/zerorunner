# -*- coding: utf-8 -*-
# @author: xiaobai
from flask import Blueprint
from autotest.utils.api import partner_success
from autotest.utils.snowflake import id_center

bp = Blueprint('id_center', __name__, url_prefix='/api/idCenter')


@bp.route('/getId', methods=['GET'])
def get_all_lookup():
    """
    获取id
    :return:
    """
    data = id_center.get_id()
    return partner_success(data=str(data))
