from config import config
from enum import Enum
from autotest.models.coverage_models import CoverageClassDetail, CoverageMethodDetail, CoverageBackendReport
from autotest.schemas.coverage.coverage_report import CoverageReportQuery, CovElTypeEenum, CoverageListQuery, \
    JacocoReportIn
from autotest.utils.async_http import AsyncHttp


class JacocoServiceApiEnum(Enum):
    StartApi = f"{config.JACOCO_SERVER_URL}/coverage/report/start"


class CoverageReportService:

    @staticmethod
    async def start(params: JacocoReportIn):
        body = {
            "reportId": "",
            "gitUserName": config.GITLAB_USER,
            "gitPassword": config.GITLAB_PASSWORD,
            "gitUrl": params.git_url,
            "newBranchName": params.new_branches,
            "newLastCommit": params.new_last_commit_id,
            "oldBranchName": params.old_branches,
            "oldLastCommit": params.old_last_commit_id,
            "diffType": "diff" if params.report_type == 20 else "full",
            "jacocoPort": 13210,
            "serverIps": ["127.0.0.1"]
        }

        coverage_report = await CoverageBackendReport.create_or_update(params.dict())
        body["reportId"] = coverage_report.get("id")
        res = await AsyncHttp().request("post", JacocoServiceApiEnum.StartApi.value, json=body)
        return res

    @staticmethod
    async def list(params: CoverageListQuery):
        return await CoverageBackendReport.get_list(params)

    @staticmethod
    async def get(id: int):
        return await CoverageBackendReport.get(id)

    @staticmethod
    def get_report_detail(params: CoverageReportQuery):
        """获取覆盖率报告详情"""
        if params.el_type == CovElTypeEenum.REPORT:
            return CoverageClassDetail.get_detail_by_report(params)
        elif params.el_type == CovElTypeEenum.PACKAGE:
            return CoverageClassDetail.get_detail_by_package(params)
        elif params.el_type == CovElTypeEenum.CLASS:
            return CoverageMethodDetail.get_detail_by_class(params)
