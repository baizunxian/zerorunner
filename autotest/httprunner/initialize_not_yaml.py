import json
import os
import sys
import uuid
from typing import Text, Dict, Any, List, Union

from loguru import logger

from autotest.config import config
from autotest.httprunner import exceptions, __version__
from autotest.httprunner.compat import ensure_testcase_v3
from autotest.httprunner.loader import load_testcase, locate_project_root_directory, load_debugtalk_functions
from autotest.httprunner.make import __ensure_testcase_module as _ensure_testcase_module, make_config_chain_style, \
    make_teststep_chain_style, __TEMPLATE__
from autotest.httprunner.models import ProjectMeta
from autotest.httprunner.parser import parse_data
from autotest.models.api_models import ProjectInfo, CaseInfo, ModuleInfo, DebugTalk
from autotest.utils.des import encrypt_rsa_password
from autotest.utils.service_utils import get_testcase_dir_path, dump_python_file, data_type_change, key_value_list


class TestCaseMateNew:
    def __init__(self, base_url: Text = ''):
        self.project_meta = None
        self.pytest_files_made_cache_mapping = {}
        self.pytest_files_run_set = set()
        self.tests_paths = []
        self.case_hex = f'testcase{uuid.uuid4().hex[:6]}'
        self.testcase_dir_path = get_testcase_dir_path()
        self.config_headers = {}
        self.testcases = []

        self.base_url = base_url
        self.name = None
        self.run_type = None
        self.summary_path = os.path.join(self.testcase_dir_path, self.case_hex, 'summary.json')
        self.project_id = None
        self.module_id = None
        self.config_id = None
        self.execute_user_id = None
        self.run_mode = None
        self.number_of_run = 1

    def run_case_make(self, case_list: List[Any]):
        for case in case_list:
            self.handle_dict_testcase(case)
        self.make()

    def debug_case_make(self, case_info):
        self.handle_dict_testcase(case_info)
        self.make()

    def make(self):
        for case in self.testcases:
            self.make_testcase(case)

    def handle_dict_testcase(self, case_info: Dict[Text, Any]):
        """
        处理用例，入库的用例处理成httpurnner用例
        :param case_info:
        :return:
        """

        testcase: Any = {
            'config': {
                'base_url': self.base_url,
                'name': '',
                'variables': {},
                'verify': False,
                'export': [],
                'path': self.testcase_dir_path,
            },
            'teststeps': []
        }

        case_id = case_info.get('id', uuid.uuid4().hex[:6])
        testcase_body = case_info.get('testcase', {})
        testcase_body['id'] = case_id
        name = case_info.get('name', '')
        include = case_info['include']
        module_id = case_info.get('module_id', None)
        project_id = case_info.get('project_id', None)

        # 关联项目配置
        project_info = ProjectInfo.get(project_id) if project_id else None
        if project_info and project_info.config_id:
            project_config = CaseInfo.get(project_info.config_id)
            if project_config:
                project_config_dict = self.make_dict_case(json.loads(project_config.testcase))
                project_headers = project_config_dict.get('request', {}).get('headers', {})
                project_variables = project_config_dict.get('variables', {})
                self.config_headers.update(project_headers)
                testcase['config']['variables'].update(project_variables)

        # 获取模块关联的配置
        module_info = ModuleInfo.get(module_id) if module_id else None
        if module_info and module_info.config_id:
            module_config = CaseInfo.get(module_info.config_id)
            if module_config:
                module_config_dict = self.make_dict_case(json.loads(module_config.testcase))
                module_headers = module_config_dict.get('request', {}).get('headers', {})
                module_variables = module_config_dict.get('variables', {})
                self.config_headers.update(module_headers)
                testcase['config']['variables'].update(module_variables)

        # 获取用例关联的配置
        config_id = case_info.get('config_id', None)
        case_config = CaseInfo.get(config_id) if config_id else None
        if case_config:
            case_config_dict = self.make_dict_case(json.loads(case_config.testcase))
            if case_config_dict:
                case_headers = case_config_dict.get('request', {}).get('headers', {})
                case_variables = case_config_dict.get('variables', {})
                self.config_headers.update(case_headers)
                testcase['config']['variables'].update(case_variables)

        testcase['config']['name'] = name

        if not os.path.exists(self.testcase_dir_path):
            os.makedirs(self.testcase_dir_path)
            path = config.BASEDIR
            function_path = os.path.join(path, 'utils', 'basic_function.py')
            try:
                debug_talk = DebugTalk.get_by_project_id(project_id)
                debug_talk = debug_talk.debug_talk if debug_talk.debug_talk else ''
            except Exception as err:
                debug_talk = ''

            with open(function_path, encoding='utf8') as func_file:
                basic_function = func_file.read()
            dump_python_file(os.path.join(self.testcase_dir_path, 'debugtalk.py'),
                             basic_function + '\n' + '\n' + debug_talk)

        _ensure_testcase_module(self.testcase_dir_path)
        testcase_dir_path = os.path.join(self.testcase_dir_path, self.case_hex)

        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        for include_id in include:
            test_case_info = CaseInfo.get(include_id)
            if test_case_info:
                pre_testcase = json.loads(test_case_info.testcase)
                # pre_testcase.get('request').pop('type')
                pre_testcase['id'] = case_id
                testcase['teststeps'].append(pre_testcase)

        if testcase_body['request']['url'] != '':
            # testcase_body.get('request').pop('type')
            testcase_body['case_id'] = case_id
            testcase['teststeps'].append(testcase_body)

        # 写入yaml文件
        testcase['teststeps'] = list(map(self.make_dict_case, testcase['teststeps']))
        self.testcases.append(testcase)

    def make_dict_case(self, kwargs: Any) -> Any:
        """
        用例格式转换
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
            req_type = request_info.pop('mode', None) or request_info.pop('type', None)
            language: Text = request_info.pop('language', None)
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

            elif req_type == 'raw':
                data = request_info.pop('data', [])
                if language.lower() == 'json':
                    data = json.loads(data) if isinstance(data, Text) else data
                    request_info.setdefault('json', data)
                elif language.lower() == 'text':
                    request_info.setdefault('data',  data.encode('utf8'))


        if 'headers' in request_info:
            headers = request_info.pop('headers', {})
            headers.update(self.config_headers)
            request_info.setdefault('headers', headers)

        if 'setup_hooks' in testcase:
            setup_hooks = testcase.pop('setup_hooks', [])
            testcase.setdefault('setup_hooks', setup_hooks)

        if 'teardown_hooks' in testcase:
            teardown_hooks = testcase.pop('teardown_hooks', [])
            testcase.setdefault('teardown_hooks', teardown_hooks)

        if 'extract' in testcase:
            extract = testcase.pop('extract', [])
            extract_dict = {}
            for ex in extract:
                extract_dict.update(ex)
            testcase.setdefault('extract', extract_dict if extract else {})

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

    def make_testcase(self, testcase: Dict):
        """
        测试用例转为py用例文件
        :param testcase:
        :param dir_path:
        :return:
        """
        testcase = ensure_testcase_v3(testcase)
        test_dir_path = os.path.join(self.testcase_dir_path, self.case_hex)
        load_testcase(testcase)
        self.load_project_meta(test_dir_path)

        testcase_python_abs_path = os.path.join(test_dir_path, f'{self.case_hex}_test.py')

        if testcase_python_abs_path in self.pytest_files_made_cache_mapping:
            return testcase_python_abs_path

        config = testcase["config"]
        config["path"] = testcase_python_abs_path
        config["variables"] = self.convert_variables(config.get("variables", {}))

        imports_list = []
        teststeps = testcase["teststeps"]

        testcase_path = testcase_python_abs_path[len(self.project_meta.RootDir) + 1:]
        # current file compared to ProjectRootDir
        diff_levels = len(testcase_path.split(os.sep))
        project_path = config.get('path', None)
        data = {
            "version": __version__,
            "testcase_path": testcase_path,
            "diff_levels": diff_levels,
            "project_path": f'{project_path}',
            "class_name": f"TestCase{self.case_hex}",
            "imports_list": imports_list,
            "config_chain_style": make_config_chain_style(config),
            "parameters": config.get("parameters"),
            "teststeps_chain_style": [
                make_teststep_chain_style(step) for step in teststeps
            ],
        }
        content = __TEMPLATE__.render(data)

        # ensure new file's directory exists
        dir_path = os.path.dirname(testcase_python_abs_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(testcase_python_abs_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.pytest_files_made_cache_mapping[testcase_python_abs_path] = self.case_hex
        _ensure_testcase_module(testcase_python_abs_path)

        logger.info(f"generated testcase: {testcase_python_abs_path}")
        self.pytest_files_run_set.add(testcase_python_abs_path)

    def load_project_meta(self, test_path: Text, reload: bool = False) -> ProjectMeta:
        """ load testcases, .env, debugtalk.py functions.
            testcases folder is relative to project_root_directory
            by default, project_meta will be loaded only once, unless set reload to true.

        Args:
            test_path (str): test file/folder path, locate project RootDir from this path.
            reload: reload project meta if set true, default to false

        Returns:
            project loaded api/testcases definitions,
                environments and debugtalk.py functions.

        """
        if self.project_meta:
            return self.project_meta

        project_meta = ProjectMeta()

        if not test_path:
            return project_meta

        debugtalk_path, project_root_directory = locate_project_root_directory(test_path)

        sys.path.insert(0, project_root_directory)
        if debugtalk_path:
            # load debugtalk.py functions
            debugtalk_functions = load_debugtalk_functions()
        else:
            debugtalk_functions = {}

        # locate project RootDir and load debugtalk.py functions
        project_meta.RootDir = project_root_directory
        project_meta.functions = debugtalk_functions
        project_meta.debugtalk_path = debugtalk_path
        self.project_meta = project_meta

        return self.project_meta

    def convert_variables(self, raw_variables: Union[Dict, List, Text]) -> Dict[Text, Any]:

        if isinstance(raw_variables, Dict):
            return raw_variables

        if isinstance(raw_variables, List):
            # [{"var1": 1}, {"var2": 2}]
            variables: Dict[Text, Any] = {}
            for var_item in raw_variables:
                if not isinstance(var_item, Dict) or len(var_item) != 1:
                    raise exceptions.TestCaseFormatError(
                        f"Invalid variables format: {raw_variables}"
                    )

                variables.update(var_item)

            return variables

        elif isinstance(raw_variables, Text):
            # get variables by function, e.g. ${get_variables()}
            variables = parse_data(raw_variables, {}, self.project_meta.functions)

            return variables

        else:
            raise exceptions.TestCaseFormatError(
                f"Invalid variables format: {raw_variables}"
            )

    def get_test_path_set(self):
        """
        后去py用例文件路径列表
        :return:
        """
        return list(self.pytest_files_run_set)

    def __del__(self):
        if self.project_meta and self.project_meta.RootDir in sys.path:
            sys.path.remove(self.project_meta.RootDir)
