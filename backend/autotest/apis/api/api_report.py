from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.api.api_report import TestReportQuery, TestReportDetailQuery, TestReportId
from autotest.services.api.api_report import ReportService

router = APIRouter()


@router.post('/list', description="测试报告列表")
async def report_list(params: TestReportQuery):
    data = await ReportService.list(params)
    return partner_success(data=data)


@router.post('/deleted', description="删除报告")
async def deleted(params: TestReportId):
    """
    删除报告
    :return:
    """
    data = await ReportService.deleted(params)
    return partner_success(data)


@router.post('/getReportDetail', description="测试报告")
async def get_report_detail(params: TestReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await ReportService.detail(params)
    return partner_success(data)


@router.post('/getReportStatistics', description="测试报告统计")
async def get_report_statistics(params: TestReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await ReportService.statistics(params)
    return partner_success(data)
