# -*- coding: utf-8 -*-
# @project: zero_autotest_backend
# @author: xiaobai
# @create time: 2022/9/13 16:47
from flask import Blueprint, request

from autotest.utils.api import partner_success
from autotest.services.toosl_services.data_source import DataSourceService

bp = Blueprint('data_source', __name__, url_prefix='/api/dataSource')


@bp.route('/sourceList', methods=['POST'])
def get_source_list():
    """
    获取所有角色数据
    :return:
    """
    data = DataSourceService.get_source_list(**request.get_json())
    return partner_success(data=data)


@bp.route('/dbList', methods=['POST'])
def get_db_list():
    """
    数据列表
    :return:
    """
    source_id = request.get_json().get('source_id', None)
    data = DataSourceService.get_db_list(source_id)
    return partner_success(data=data)


@bp.route('/tableList', methods=['POST'])
def get_table_list():
    """
    表列表
    :return:
    """
    source_id = request.get_json().get('source_id', None)
    databases = request.get_json().get('databases', None)
    data = DataSourceService.get_table_list(source_id, databases)
    return partner_success(data=data)


@bp.route('/columnList', methods=['POST'])
def get_column_list():
    """
    表列表
    :return:
    """
    source_id = request.get_json().get('source_id', None)
    databases = request.get_json().get('databases', None)
    data = DataSourceService.get_column_list(source_id, databases)
    return partner_success(data=data)


@bp.route('/mysql/execute', methods=['POST'])
def mysql_execute():
    """
    查询
    :return:
    """
    data = DataSourceService.execute(**request.get_json())
    return partner_success(data=data)
