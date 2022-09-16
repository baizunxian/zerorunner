from typing import Dict, Any, Union, Text

from autotest.models.api_models import TestSuite
from autotest.serialize.api_serializes.test_suites import TestSuitesListSchema, TestSuitesQuerySchema, \
    TestSuitesSaveOrUpdateSchema
from autotest.utils.api import parse_pagination


class TestSuitesService:
    @staticmethod
    def list(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = TestSuitesQuerySchema(**kwargs).dict()
        data = parse_pagination(TestSuite.get_list(**parsed_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': TestSuitesListSchema.serialize(_result)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> "TestSuite":
        """更新保存套件"""
        parsed_data = TestSuitesSaveOrUpdateSchema(**kwargs)
        #  套件名称唯一性校验
        test_suite = TestSuite.get(parsed_data.id) if parsed_data.id else TestSuite()
        test_suite.update(**parsed_data.dict())
        return test_suite

    @staticmethod
    def deleted(s_id: Union[str, int]):
        test_suite = TestSuite.get(s_id)
        test_suite.delete() if test_suite else ...

    @staticmethod
    def get_suite_info(**kwargs: Any) -> Dict[Text, Any]:
        parsed_data = TestSuitesQuerySchema(**kwargs)
        test_suite = TestSuite.get(parsed_data.id) if parsed_data.id else None
        if test_suite:
            data = TestSuitesListSchema.serialize(test_suite)
            return data
        raise ValueError('不存在当前套件！')

    @staticmethod
    def run_suites():
        ...
