from typing import Dict, Any, Union, Text

from autotest.models.api_models import TestSuite
from autotest.serialize.api_serializes.test_suites import TestSuitesListSchema, TestSuitesQuerySchema, \
    TestSuitesSaveOrUpdateSchema
from autotest.utils.api import parse_pagination


class TestSuitesService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = TestSuitesQuerySchema().load(kwargs)
        data = parse_pagination(TestSuite.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': TestSuitesListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "TestSuite":
        """更新保存套件"""
        parsed_data = TestSuitesSaveOrUpdateSchema().load(kwargs)
        #  套件名称唯一性校验
        s_id = parsed_data.get('id', None)
        test_suite = TestSuite.get(s_id) if s_id else TestSuite()
        test_suite.update(**parsed_data)
        return test_suite

    @staticmethod
    def deleted(s_id: Union[str, int]):
        test_suite = TestSuite.get(s_id)
        test_suite.delete() if test_suite else ...

    @staticmethod
    def get_suite_info(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = TestSuitesQuerySchema().load(kwargs)
        s_id = parsed_data.get('id', None)
        test_suite = TestSuite.get(s_id) if s_id else None
        if test_suite:
            data = TestSuitesListSchema().dump(test_suite)
            return data
        raise ValueError('不存在当前套件！')

    @staticmethod
    def run_suites():
        ...
