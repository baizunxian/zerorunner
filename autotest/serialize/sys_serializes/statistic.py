from marshmallow import Schema, fields


class StatisticProjectCaseNum(Schema):
    name = fields.Str()
    case_num = fields.Int()
    employee_code = fields.Str()
    username = fields.Str()


class StatisticReportNum(Schema):
    run_num = fields.Int()
    employee_code = fields.Str()
    username = fields.Str()
    case_num = fields.Str()


class StatisticReportRate(Schema):
    project_name = fields.Str()
    pass_rate = fields.Float()
    successes_rate = fields.Float()
