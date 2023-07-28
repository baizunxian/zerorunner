from autotest.services.api.api_case import ApiCaseService
from autotest.services.api.api_info import ApiInfoService
from autotest.services.api.timed_task import TimedTasksService
from autotest.services.ui.ui_case import UiCaseServer


class StatisticService:
    """统计类"""

    @staticmethod
    async def personal_statistics():
        """个人统计"""
        api_count = await ApiInfoService.get_count_by_user()
        api_case_count = await ApiCaseService.get_count_by_user()
        ui_case_count = await UiCaseServer.get_count_by_user()
        task_count = await TimedTasksService.get_count_by_user()
        data = {
            "api_count": api_count,
            "api_ratio": 0,
            "api_case_count": api_case_count,
            "api_case_ratio": 0,
            "ui_case_count": ui_case_count,
            "ui_case_ratio": 0,
            "task_count": task_count,
            "task_ratio": 0,
        }
        return data
