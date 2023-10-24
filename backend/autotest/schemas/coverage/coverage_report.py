from enum import Enum

from pydantic import Field, BaseModel


class CovElTypeEenum(str, Enum):
    """覆盖率元素类型"""

    REPORT = "report"
    PACKAGE = "package"
    CLASS = "class"
    METHOD = "method"


class CoverageListQuery(BaseModel):
    name: str = Field(None, description="name")
    id: int = Field(None, description="id")


class CoverageReportQuery(BaseModel):
    id: int = Field(None, description="id")
    el_type: str = Field(..., description="类型")
    report_id: int = Field(..., description="报告id")
    package_name: str = Field(None, description="包名")
    class_id: int = Field(None, description="类id")


class JacocoReportIn(BaseModel):
    id: int = Field(None, description="id")
    name: str = Field(None, description="name")
    git_url: str = Field(None, description="git_url")
    report_type: int = Field(None, description="report_type")
    new_branches: str = Field(None, description="比对分支")
    new_last_commit_id: str = Field(None, description="比对分支最后一次提交")
    old_branches: str = Field(None, description="基准分支")
    old_last_commit_id: str = Field(None, description="基准分支最后一次提交")
    jacoco_port: int = Field(None, description="jacoco_port")
    server_ips: list = Field(None, description="server_ips")
