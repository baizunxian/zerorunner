from typing import Optional, Text
from pydantic import BaseModel


class StatisticProjectCaseNum(BaseModel):
    name: Optional[Text]
    case_num: Optional[int]
    employee_code: Optional[Text]
    username: Optional[Text]


class StatisticReportNum(BaseModel):
    run_num: Optional[int]
    employee_code: Optional[Text]
    username: Optional[Text]
    case_num: Optional[Text]


class StatisticReportRate(BaseModel):
    project_name: Optional[Text]
    pass_rate: Optional[float]
    successes_rate: Optional[float]
