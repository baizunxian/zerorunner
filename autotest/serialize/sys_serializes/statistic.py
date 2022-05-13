from marshmallow import Schema, fields


class StatisticProjectCaseNum(Schema):
    name = fields.Str()
    case_num = fields.Int()
    employee_code = fields.Str()
    username = fields.Str()
