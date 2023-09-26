from fastapi import APIRouter, Body

from autotest.utils.response.http_response import partner_success
from autotest.schemas.coverage.coverage_report import CoverageReportQuery, CoverageListQuery, JacocoReportIn
from autotest.services.coverage.coverage_report import CoverageReportService

router = APIRouter()


@router.post('/coverageStart', description="开始覆盖率")
async def get_repository_list(params: JacocoReportIn):
    data = await CoverageReportService.start(params)
    return partner_success(data)


@router.post('/getReportList', description="获取报告详情")
async def get_report_detail(params: CoverageListQuery):
    data = await CoverageReportService.list(params)
    return partner_success(data)


@router.post('/getReportById', description="获取报告详情")
async def get_report_detail(body=Body(...)):
    data = await CoverageReportService.get(body.get("id", None))
    return partner_success(data)


@router.post('/getCoverageDetail', description="获取覆盖详情")
async def get_report_detail(params: CoverageReportQuery):
    data = await CoverageReportService.get_report_detail(params)
    return partner_success(data)
