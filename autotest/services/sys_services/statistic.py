import datetime

from sqlalchemy import text

from autotest.models.api_models import ProjectInfo, ModuleInfo, CaseInfo, TestSuite, TestReports
from autotest.models.sys_models import User
from autotest.serialize.sys_serializes.statistic import StatisticProjectCaseNum, StatisticReportNum, StatisticReportRate
from autotest.utils.basic_function import get_today_start, get_today_end


class StatisticService:
    """统计类"""

    @staticmethod
    def index_count_statistic():
        """获取首页统计数据"""
        today_start_time = get_today_start()
        today_end_time = get_today_end()
        # 项目统计
        project_count = ProjectInfo.get_all_count()
        # 模块统计
        module_count = ModuleInfo.get_all_count()
        # 用例统计
        case_count = CaseInfo.get_all_count()
        # 套件统计
        suite_count = TestSuite.get_all_count()

        # 当天执行数
        test_ex_data = StatisticService.get_case_execution_by_time(today_start_time, today_end_time)

        # 新增用例数
        add_case_count = CaseInfo.get_case_by_time(today_start_time, today_end_time).count()

        # case 分布
        pcn_sql = CaseInfo.statistic_project_case_number()
        pcns_data = pcn_sql.group_by(ProjectInfo.name).order_by(text('case_num desc')).all()
        ucns_data = pcn_sql.group_by(User.nickname).order_by(text('case_num desc')).all()

        # 套件分布
        scn_sql = TestSuite.statistic_project_suite_number()
        scns_data = scn_sql.group_by(ProjectInfo.name).order_by(text('case_num asc')).all()

        #  project top
        pcns_data = StatisticProjectCaseNum().dump(pcns_data, many=True)

        # user top
        ucns_data = StatisticProjectCaseNum().dump(ucns_data, many=True)

        # 套件top
        scns_data = StatisticProjectCaseNum().dump(scns_data, many=True)

        # 运行用例报告统计 根据人
        report_statistic_data = TestReports.statistic_report().group_by(TestReports.execute_user_id).order_by(
            text('run_num desc')).limit(10).all()
        report_statistic = StatisticReportNum().dump(report_statistic_data, many=True)

        report_rate = TestReports.get_statistic_report().all()
        project_rate = StatisticReportRate().dump(report_rate, many=True)

        data = {
            'count_info': {
                'project_count': project_count,
                'module_count': module_count,
                'case_count': case_count,
                'suite_count': suite_count,
                'today_total_run': test_ex_data.get('total_run', 0),
                'today_run_count': test_ex_data.get('count', 0),
                'add_case_count': add_case_count,
            },
            'top_info': {
                'pcns_data': pcns_data,
                'ucns_data': ucns_data,
                'scns_data': scns_data,
            },
            'report_info': report_statistic,
            'case_run_info': StatisticService.get_case_exe_results(),
            'project_rate': project_rate
        }
        return data

    @staticmethod
    def get_case_execution_by_time(begin_time, end_time):
        """根据时间获取报告数"""
        results = {
            'time': 0,
            'pass': 0,
            'fail': 0,
            'percent': 0,
            'count': 0,
            'total_run': 0,
        }
        report_all = TestReports.get_report_by_time(begin_time, end_time)
        total_run = 0
        pass_count = 0
        for report in report_all.all():
            if begin_time <= report.start_at.strftime('%Y-%m-%d %H:%M:%S') <= end_time:
                total_run += report.run_test_count if report.run_test_count else 0
                pass_count += report.successful_use_case if report.successful_use_case else 0
        results['date'] = begin_time
        results['pass'] = pass_count
        results['fail'] = total_run - pass_count
        results['percent'] = round(pass_count / total_run * 100, 2) if total_run != 0 else 0.00
        results['count'] = report_all.count()
        results['total_run'] = total_run
        return results

    @staticmethod
    def get_case_exe_results():
        """测试报告执行数据"""
        results = {
            'date': [],
            'pass': [],
            'fail': [],
            'percent': [],
            'run_count': [],
            'module_exe_num': [],
            'case_exe_num': [],
            'suite_exe_num': [],
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
            module_exe_num = 0
            case_exe_num = 0
            suite_exe_num = 0
            for report in report_all:
                if begin_time <= report.start_at.strftime('%Y-%m-%d %H:%M:%S') <= end_time:
                    total_run += report.run_test_count if report.run_test_count else 0
                    pass_count += report.successful_use_case if report.successful_use_case else 0
                    if report.run_type == 'module':
                        module_exe_num += 1
                    if report.run_type == 'case':
                        case_exe_num += 1
                    if report.run_type == 'suite':
                        suite_exe_num += 1
            results['date'].append(c_time.strftime('%Y-%m-%d'))
            results['pass'].append(pass_count)
            results['fail'].append(total_run - pass_count)
            results['run_count'].append(module_exe_num + case_exe_num + suite_exe_num)
            results['percent'].append(round(pass_count / total_run * 100, 2) if total_run != 0 else 0.00)
            results['module_exe_num'].append(module_exe_num)
            results['case_exe_num'].append(case_exe_num)
            results['suite_exe_num'].append(suite_exe_num)
        return results
