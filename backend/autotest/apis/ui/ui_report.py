from fastapi import APIRouter

from autotest.utils.response.http_response import partner_success
from autotest.schemas.ui.ui_report import UiReportQuery, UiReportId, UiReportDetailQuery
from autotest.services.ui.ui_report import UiReportService

router = APIRouter()


@router.post('/list', description="测试报告列表")
async def report_list(params: UiReportQuery):
    data = await UiReportService.list(params)
    return partner_success(data=data)


@router.post('/deleted', description="删除报告")
async def deleted(params: UiReportId):
    """
    删除报告
    :return:
    """
    data = await UiReportService.deleted(params)
    return partner_success(data)


@router.post('/getUiReportDetail', description="测试报告")
async def get_report_detail(params: UiReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await UiReportService.detail(params)
    return partner_success(data)


@router.post('/getUiReportStatistics', description="测试报告统计")
async def get_report_statistics(params: UiReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await UiReportService.statistics(params)
    return partner_success(data)
