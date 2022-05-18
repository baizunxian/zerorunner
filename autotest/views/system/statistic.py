import datetime
import traceback

from flask import Blueprint, request
from loguru import logger

from autotest.exc import codes
from autotest.services.sys_services.statistic import StatisticService
from autotest.utils.api import login_verification, json_required, partner_success

bp = Blueprint('statistic', __name__, url_prefix='/api/statistic')


@bp.route('/countStatistic', methods=['POST'])
@login_verification
@json_required
def count_statistic():
    """数量统计"""
    try:
        data = StatisticService.index_count_statistic()
    except Exception as err:
        logger.error(traceback.format_exc())
        return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
    return partner_success(data=data)


@bp.route('/statistic/useCET', methods=['POST'])
@login_verification
@json_required
def use_case_execution_trend():
    """userCET"""
    "Use case execution trend"
    data = get_case_exe_results()
    return partner_success(data)


@bp.route('/CaseExecutionResults', methods=['POST'])
@login_verification
@json_required
def case_execution_results():
    """测试报告执行数据"""
    results = {
        'date': [],
        'pass': [],
        'fail': [],
        'percent': [],
    }
    today = datetime.date.today()
    b_time = today + datetime.timedelta(days=-12)
    report_all = TestReports.get_report_by_time(b_time.strftime('%Y-%m-%d 00:00:00'),
                                                today.strftime('%Y-%m-%d 23:59:59')).all()
    # todo : 这种方式小数据量效果会比较好，数据量大的话要重新优化
    for i in range(-11, 1):
        c_time = (today + datetime.timedelta(days=i))
        begin_time = c_time.strftime('%Y-%m-%d 00:00:00')
        end_time = c_time.strftime('%Y-%m-%d 23:59:59')
        total_run = 0
        pass_count = 0
        for report in report_all:
            if begin_time <= report.start_at.strftime('%Y-%m-%d %H:%M:%S') <= end_time:
                total_run += report.test_count if report.test_count else 0
                pass_count += report.successes_test_count if report.successes_test_count else 0

        results['date'].append(c_time.strftime('%Y-%m-%d'))
        results['pass'].append(pass_count)
        results['fail'].append(total_run - pass_count)
        results['percent'].append(round(pass_count / total_run * 100, 2) if total_run != 0 else 0.00)

    # 这种模式查询数据库比较多，导致响应比较慢
    # today = datetime.date.today()
    # for i in range(-11, 1):
    #     begin_time = today + datetime.timedelta(days=i)
    #     end_time = begin_time + datetime.timedelta(days=1)
    #
    #     report_query = TestReports.get_report_by_time(begin_time, end_time)
    #     total_run = report_query.count()
    #     total_success = report_query.filter(TestReports.successes == 'success').count()
    #
    #     total_percent = round(total_success / total_run * 100, 2) if total_run != 0 else 0.00
    #     results['date'].append(begin_time.strftime('%Y-%m-%d'))
    #     results['pass'].append(total_success)
    #     results['fail'].append(total_run - total_success)
    #     results['percent'].append(total_percent)
    return partner_success(results)


@bp.route('/moduleStatisticsReport', methods=['POST'])
def module_statistics_report():
    parsed_data = request.json
    module_name = parsed_data.get('module_name', None)
    project_name = parsed_data.get('project_name', None)
    module_packages = parsed_data.get('module_packages', None)
    sort_type = parsed_data.get('sort_type', None)
    order_field = parsed_data.get('order_field', None)
    data = parse_pagination(
        ModuleInfo.module_statistics(module_name, project_name, module_packages, order_field, sort_type))
    _result, pagination = data.get('result'), data.get('pagination')
    _result = ModuleStatisticsReportSchema().dump(_result, many=True)
    data_list = []
    for result in _result:
        cicd_info = CicdInfo.get_by_module_packages(result['module_packages'])
        if cicd_info:
            report = TestReports.get(cicd_info.report_id)
            if report:
                result['success_rate'] = (
                                                 report.successes_test_count / report.test_count) * 100 if report.test_count != 0 else 0
            else:
                result['success_rate'] = 0
        else:
            result['success_rate'] = 0
        data_list.append(result)
    result = {
        'rows': data_list
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/productStatisticsReport', methods=['POST'])
@login_verification
@json_required
def product_statistics_report():
    """产品线分析报表"""
    parsed_data = request.json
    min_and_max = parsed_data.get('min_and_max', None)
    sort_type = parsed_data.get('sort_type', None)
    order_field = parsed_data.get('order_field', None)
    data = parse_pagination(ReportProduct.get_statistics_list(min_and_max, order_field, sort_type))
    _result, pagination = data.get('result'), data.get('pagination')
    _result = ProductStatisticsSchema().dump(_result, many=True)
    result = {
        'rows': _result
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/moduleStatisticsReportNew', methods=['POST'])
@json_required
def module_statistics_report_new():
    """模块分析报表"""
    parsed_data = request.json
    min_and_max = parsed_data.get('min_and_max', None)
    sort_type = parsed_data.get('sort_type', None)
    order_field = parsed_data.get('order_field', None)
    module_name = parsed_data.get('module_name', None)
    project_name = parsed_data.get('project_name', None)
    packages_name = parsed_data.get('packages_name', None)
    data = parse_pagination(ReportModule.get_statistics_list(min_and_max, order_field, sort_type,
                                                             module_name=module_name,
                                                             project_name=project_name, packages_name=packages_name))
    _result, pagination = data.get('result'), data.get('pagination')
    _result = ModuleStatisticsSchema().dump(_result, many=True)
    result = {
        'rows': _result
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/productStatisticsHand', methods=['POST'])
@json_required
def product_statistics_hand():
    parsed_data = request.json
    day = parsed_data.get('day', None)
    report_type = parsed_data.get('type', None)
    if report_type == 'module':
        report_task(day)
    else:
        product_report_task(day)
    return partner_success()


@bp.route('/CICDStatisticsReport', methods=['POST'])
@json_required
# @login_verification
def cicd_statistics_report():
    parsed_data = request.json
    params = {
        'module_packages': parsed_data.get('module_packages', None)
    }
    data = get_report_data(**params)
    _result, pagination = data.get('result'), data.get('pagination')
    _result = CICDStatisticReportForm().dump(_result, many=True)
    result = {
        'rows': _result
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/genericStatisticsReport', methods=['POST'])
@json_required
def generic_statistics_report():
    """通用查询分析报表"""
    parsed_data = request.json
    min_and_max = parsed_data.get('min_and_max', None)
    sort_type = parsed_data.get('sort_type', None)
    order_field = parsed_data.get('order_field', None)
    data = parse_pagination(ReportGeneric.get_statistics_list(min_and_max, order_field, sort_type))
    _result, pagination = data.get('result'), data.get('pagination')
    _result = GenericStatisticsSchema().dump(_result, many=True)
    result = {
        'rows': _result
    }
    result.update(pagination)
    return partner_success(result)


@bp.route('/genericReport', methods=['POST'])
@json_required
def get_group_generic_report():
    """按日期统计通用查询运营数据"""
    parsed_data = request.json
    day = parsed_data.get('day', None)
    report_generic_statistic(day)
    return partner_success()


@bp.route('/genericReportExcel', methods=['POST'])
@json_required
def generic_report_excel():
    """通用查询报表数据导出excel"""
    parsed_data = request.json
    min_and_max = parsed_data.get('min_and_max', None)
    data = GenericStatisticsSchema().dump(ReportGeneric.get_statistics_list(min_and_max), many=True)

    column = ['product_name', 'case_count', 'report_detail_count', 'report_detail_success', 'report_detail_fail',
              'pass_rate']
    col_name = ['产品线', '用例数', '报告总数', '成功数', '失败数', '成功率']
    response = generate_table(data, column, col_name)
    response.headers['Content-type'] = 'application/vnd.ms-excel'  # 响应头告诉浏览器发送的文件类型为excel
    response.headers['Content-Disposition'] = 'attachment; filename=newlist.xlsx'  # 浏览器打开/保存的对话框，data.xlsx-设定的文件名

    return response
