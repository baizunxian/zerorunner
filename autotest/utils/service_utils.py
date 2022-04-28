import io
import json
import os
import uuid
from typing import Any, Union, Dict, Text

import yaml

from autotest.config import config
from autotest.httprunner.make import __ensure_testcase_module as _ensure_testcase_module
from autotest.models.api_models import CaseInfo, ModuleInfo, ProjectInfo, DebugTalk
from autotest.utils.common import get_timestamp
from autotest.utils.des import encrypt_rsa_password


class DumpTestCase:

    def __init__(self, case_info: Dict, base_url: str, testcase_dir_path: str, case_hex: str,
                 number_of_run: Union[int, None] = None):
        """
        加载单个case用例信息
        :param case_info: dict：运行用例信息
        :param base_url: str：环境地址
        :param testcase_dir_path: str：文件路径
        :param case_hex: str：环境地址
        :param number_of_run: str：运行次数
        :return: dict
        """
        self._case_info = case_info
        self._base_url = base_url
        self._testcase_dir_path = testcase_dir_path
        self._case_hex = case_hex
        self._number_of_run = number_of_run
        self._config_headers = {}
        self._testcase = {
            'config': {
                'base_url': self._base_url,
                'name': '',
                'variables': {},
                'verify': False,
                'export': [],
            },
            'teststeps': []
        }
        self.dict_testcase_2_yaml()

    def dict_testcase_2_yaml(self) -> Text:

        case_id = self._case_info.get('id', uuid.uuid4().hex[:6])
        testcase_body = self._case_info.get('testcase', {})
        testcase_body['id'] = case_id
        name = self._case_info.get('name', '')
        include = self._case_info['include']
        module_id = self._case_info.get('module_id', None)
        project_id = self._case_info.get('project_id', None)

        # 关联项目配置
        project_info = ProjectInfo.get(project_id) if project_id else None
        if project_info and project_info.config_id:
            project_config = CaseInfo.get(project_info.config_id)
            if project_config:
                project_config_dict = self.make_testcase(json.loads(project_config.testcase))
                project_headers = project_config_dict.get('request', {}).get('headers', {})
                project_variables = project_config_dict.get('variables', {})
                self._config_headers.update(project_headers)
                self._testcase['config']['variables'].update(project_variables)

        # 获取模块关联的配置
        module_info = ModuleInfo.get(module_id) if module_id else None
        if module_info and module_info.config_id:
            module_config = CaseInfo.get(module_info.config_id)
            if module_config:
                module_config_dict = self.make_testcase(json.loads(module_config.testcase))
                module_headers = module_config_dict.get('request', {}).get('headers', {})
                module_variables = module_config_dict.get('variables', {})
                self._config_headers.update(module_headers)
                self._testcase['config']['variables'].update(module_variables)

        # 获取用例关联的配置
        config_id = self._case_info.get('config_id', None)
        case_config = CaseInfo.get(config_id) if config_id else None
        if case_config:
            case_config_dict = self.make_testcase(json.loads(case_config.testcase))
            if case_config_dict:
                case_headers = case_config_dict.get('request', {}).get('headers', {})
                case_variables = case_config_dict.get('variables', {})
                self._config_headers.update(case_headers)
                self._testcase['config']['variables'].update(case_variables)

        self._testcase['config']['name'] = name

        if not os.path.exists(self._testcase_dir_path):
            os.makedirs(self._testcase_dir_path)
            path = config.BASEDIR
            function_path = os.path.join(path, 'utils', 'basic_function.py')
            try:
                debug_talk = DebugTalk.get_by_project_id(project_id)
                debug_talk = debug_talk.debug_talk if debug_talk.debug_talk else ''
            except Exception as err:
                debug_talk = ''

            with open(function_path, encoding='utf8') as func_file:
                basic_function = func_file.read()
            dump_python_file(os.path.join(self._testcase_dir_path, 'debugtalk.py'),
                             basic_function + '\n' + '\n' + debug_talk)

        _ensure_testcase_module(self._testcase_dir_path)
        testcase_dir_path = os.path.join(self._testcase_dir_path, self._case_hex)

        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        for include_id in include:
            test_case_info = CaseInfo.get(include_id)
            if test_case_info:
                pre_testcase = json.loads(test_case_info.testcase)
                # pre_testcase.get('request').pop('type')
                pre_testcase['id'] = case_id
                self._testcase['teststeps'].append(pre_testcase)

        if testcase_body['request']['url'] != '':
            # testcase_body.get('request').pop('type')
            testcase_body['case_id'] = case_id
            self._testcase['teststeps'].append(testcase_body)

        # 写入yaml文件
        self._testcase['teststeps'] = list(map(self.make_testcase, self._testcase['teststeps']))
        for i in (range(int(self._number_of_run) if self._number_of_run else 1)):
            dump_yaml_file(os.path.join(testcase_dir_path, f'test_case{case_id}{uuid.uuid4().hex[:6]}{i}.yml'),
                           self._testcase)

        return testcase_dir_path

    def make_testcase(self, kwargs: Any) -> Any:
        """
        生成测试用例
        :param kwargs: dict: 用例信息
        :param config_headers: dict: 配置请求头
        :return: str: ok or tips
        """
        testcase = kwargs
        if not testcase:
            raise ValueError('错误的用例格式！')

        kwargs['include'] = ','.join(kwargs['include']) if kwargs.get('include', None) else None

        request_info = testcase.get('request', {})
        if request_info:
            req_type = request_info.pop('type', None)
            if req_type == 'params':
                params_data = request_info.pop('params', [])
                params_dict = {}
                for data in params_data:
                    params_type = data.pop('type')
                    params_value = data.pop('value')
                    params_key = data.pop('key')
                    value = data_type_change(params_type, params_value)
                    if value == 'exception':
                        raise ValueError('{}:{} 类型错误,不是{}类型'.format(params_key, params_value, params_type))
                    params_dict[params_key] = value
                request_info.setdefault('params', params_dict)

            elif req_type == 'form_data':
                form_data = request_info.pop('form_data', [])
                upload_dict = {}
                for data in form_data:
                    data_type = data.pop('type')
                    data_value = data.pop('value')
                    data_key = data.pop('key')
                    if data_type == 'file':
                        abspath = data_value.get('abspath', '')
                        file_name = data_value.get('name', '')
                        if not os.path.exists(abspath):
                            raise FileNotFoundError(f'文件 {file_name} 找不到~')
                        upload_dict[data_key] = data_value.get('abspath', '')
                    else:
                        upload_dict[data_key] = data_value
                request_info.setdefault('upload', upload_dict)

        if 'headers' in request_info:
            headers = request_info.pop('headers', {})
            headers.update(self._config_headers)
            request_info.setdefault('headers', headers)

        if 'setup_hooks' in testcase:
            setup_hooks = testcase.pop('setup_hooks', [])
            testcase.setdefault('setup_hooks', setup_hooks)

        if 'teardown_hooks' in testcase:
            teardown_hooks = testcase.pop('teardown_hooks', [])
            testcase.setdefault('teardown_hooks', teardown_hooks)

        if 'extract' in testcase:
            extract = testcase.pop('extract', [])
            testcase.setdefault('extract', extract)

        if 'validate' in testcase:
            validate = testcase.pop('validate')
            validate_list = []
            for validate_dict in validate:
                validate_type = validate_dict.pop('type')
                validate_value = validate_dict.pop('expected')
                value = data_type_change(validate_type, validate_value)
                if value == 'exception':
                    raise ValueError('{}:{} 类型错误,不是{}类型'.format(validate_dict['check'], validate_value, validate_type))
                validate_dict['expected'] = value
                v_info = {validate_dict['comparator']: [validate_dict['check'], validate_dict['expected']]}
                validate_list.append(v_info)
            testcase.setdefault('validate', validate_list)

        if 'variables' in testcase:
            variables = testcase.pop('variables')
            variables_dict = {}
            for variable in variables:
                variables_key = variable.pop('key')
                variables_type = variable.pop('type')
                variables_value = variable.pop('value')
                remarks = variable.pop('remarks_')
                value = data_type_change(variables_type, variables_value)
                if value == 'exception':
                    raise ValueError('{}:{} 类型错误,不是{}类型'.format(variables_key, variables_value, variables_type))

                # 判断__encryption 是否包涵，如果包涵 加密处理
                # todo 当value 等于172位时，会有问题
                if '__encryption' in variables_key and len(value) != 172:
                    variable[variables_key] = str(encrypt_rsa_password(value), encoding='utf8')
                else:
                    variable[variables_key] = value
                variables_dict.update(variable)
            testcase.setdefault('variables', variables_dict)

        if 'parameters' in testcase:
            parameters = testcase.pop('parameters')

            parameters = {'testcase': parameters}
            params_list = key_value_list('parameters', **parameters)
            if not isinstance(params_list, list):
                return params_list
            params_dict = {}
            for params in params_list:
                if 'remarks_' in params:
                    params.pop('remarks_')
                params_dict.update(params)

            testcase.setdefault('parameters', params_dict)

        return kwargs


# 递归合并配置信息方法
def merge_config(basic_config, new_config):
    if type(basic_config) is dict and type(new_config) is dict:
        for config in basic_config:
            if config not in new_config:
                new_config[config] = basic_config[config]
            elif len(basic_config.keys()) > 0:
                merge_config(basic_config[config], new_config[config])
    elif type(basic_config) is list and type(new_config) is list:
        new_config[0:0] = basic_config


def check_testcase(**kwargs: Any):
    """
    用例入库前校验
    :param kwargs: dict: 用例信息
    :return: str: ok or tips
    """

    request_info = kwargs.get('request', {})
    if request_info:
        if request_info.get('type') == 'params':
            params_data = request_info.get('params', [])
            for data in params_data:
                params_type = data.get('type')
                params_value = data.get('value')
                params_key = data.get('key')
                value = data_type_change(params_type, params_value)
                if value == 'exception':
                    raise ValueError('{}:{} 类型错误,不是{}类型'.format(params_key, params_value, params_type))

    if kwargs.get('validate', None):
        validate = kwargs.get('validate')
        for validate_dict in validate:
            validate_type = validate_dict.get('type')
            validate_value = validate_dict.get('expected')
            value = data_type_change(validate_type, validate_value)
            if value == 'exception':
                raise ValueError('{}:{} 类型错误,不是{}类型'.format(validate_dict['check'], validate_value, validate_type))

    if kwargs.get('variables', None):
        variables = kwargs.get('variables')
        for variables_dict in variables:
            variables_key = variables_dict.get('key')
            variables_type = variables_dict.get('type')
            variables_value = variables_dict.get('value')
            remarks = variables_dict.get('remarks_')
            value = data_type_change(variables_type, variables_value)
            if value == 'exception':
                raise ValueError('{}:{} 类型错误,不是{}类型'.format(variables_key, variables_value, variables_type))


def data_type_change(data_type: str, value: Any):
    """
    数据类型转换
    :param data_type: str: 类型
    :param value: object: 待转换的值
    :return: ok or error
    """
    data_type = data_type.lower()
    if data_type == 'boolean':
        if value == 'False' or value == 'false' or value is False:
            value = False
        elif value == 'True' or value == 'true' or value is True:
            value = True
        else:
            return 'exception'
    try:
        if data_type == 'float':
            value = float(value)
        elif data_type == 'int':
            value = int(value)
        elif data_type == 'dict' or data_type == 'list':
            value = json.loads(value)
    except ValueError:
        return 'exception'
    return value


def key_value_list(keyword: str, **kwargs):
    """
    dict change to list
    :param keyword: str: 关键字标识
    :param kwargs: dict: 待转换的字典
    :return: ok or tips
    """
    if not isinstance(kwargs, dict) or not kwargs:
        return None
    else:
        lists = []
        test = kwargs.pop('testcase')
        for value in test:
            if keyword == 'setup_hooks':
                if value.get('key') != '':
                    lists.append(value.get('key'))
            elif keyword == 'teardown_hooks':
                if value.get('value') != '':
                    lists.append(value.get('value'))
            else:
                key = value.pop('key')
                val = value.pop('value')
                if 'type' in value.keys():
                    data_type = value.pop('type')
                else:
                    data_type = 'str'
                tips = '{keyword}: {val}格式错误,不是{type}类型'.format(keyword=keyword, val=val, type=data_type)
                if key != '':
                    if keyword == 'validate':
                        value['check'] = key
                        msg = data_type_change(data_type, val)
                        if msg == 'exception':
                            return tips
                        value['expected'] = msg
                    elif keyword == 'extract':
                        value[key] = val
                    elif keyword == 'variables':
                        msg = data_type_change(data_type, val)
                        if msg == 'exception':
                            return tips
                        value[key] = msg
                    elif keyword == 'parameters':
                        try:
                            if not isinstance(eval(val), list):
                                raise ValueError('{keyword}: {val}格式错误'.format(keyword='参数', val=val))
                            value[key] = eval(val)
                        except Exception:
                            value[key] = val
                            # raise ValueError('{keyword}: {val}格式错误'.format(keyword='参数', val=val))
                lists.append(value)
        return lists


def dump_yaml_file(yaml_file, data):
    """加载yaml文件并检查文件内容格式"""
    with io.open(yaml_file, 'w', encoding='utf-8') as stream:
        yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8')


def dump_python_file(python_file, data):
    """存储python文件"""
    with io.open(python_file, 'w', encoding='utf-8') as stream:
        stream.write(data)


def get_testcase_dir_path() -> Text:
    """
    生成用例运行地址
    :return:
    """
    return os.path.join(config.TEST_DIR, f'run_test_{get_timestamp()}')
