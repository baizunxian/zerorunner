import os
import string
import sys
from typing import Dict, Text, List, Tuple, Union, Any, Set

from loguru import logger

from autotest.httprunner import Config as HrConfig, RunRequest, exceptions, __version__
from autotest.httprunner import HttpRunner
from autotest.httprunner.compat import ensure_path_sep, ensure_testcase_v3_api, ensure_testcase_v3
from autotest.httprunner.loader import load_folder_files, load_test_file, load_testcase, \
    load_debugtalk_functions, locate_project_root_directory
from autotest.httprunner.make import __ensure_testcase_module as _ensure_testcase_module
from autotest.httprunner.make import make_config_chain_style, make_teststep_chain_style, __TEMPLATE__
from autotest.httprunner.models import ProjectMeta
from autotest.httprunner.parser import parse_data
from autotest.httprunner.response import uniform_validator
from autotest.httprunner.testcase import RequestWithOptionalArgs, Step, RunTestCase


class TestCaseRunner(HttpRunner):
    def __init__(self, case_info_data: Dict):
        super(TestCaseRunner, self).__init__()
        self.__case_info: Dict = case_info_data

    def run_test(self):
        self._init_config()
        self._init_teststeps()
        self.run()

    def _init_config(self):
        """
        init config
        :return:
        """
        config_dict = self.__case_info.get('config', None)
        if not config_dict:
            raise exceptions.ParamsError('-----lack config-----')
        name = config_dict.get('name', 'test case')
        config = HrConfig(name)

        if config_dict.get('variables', None):
            variables = config_dict.pop('variables')
            config.variables(**variables)

        if "base_url" in config_dict:
            config.base_url(config_dict.get('base_url'))

        if "verify" in config_dict:
            config.verify(config_dict.get('verify'))

        if "export" in config_dict:
            config.export(*config_dict.get('export'))

        if "weight" in config_dict:
            config.locust_weight(config_dict.get('weight'))
        self.config = config

    @staticmethod
    def _init_request(request: Dict, step_info: RequestWithOptionalArgs) -> "RequestWithOptionalArgs":
        """
        init request
        :param request: request info
        :param step_info: step_info object
        :return:
        """
        if "params" in request:
            params = request["params"]
            step_info.with_params(**params)

        if "headers" in request:
            headers = request["headers"]
            step_info.with_headers(**headers)

        if "cookies" in request:
            cookies = request["cookies"]
            step_info.with_cookies(**cookies)

        if "data" in request:
            data = request["data"]
            if isinstance(data, Text):
                data = f'"{data}"'
            step_info.with_data(data)

        if "json" in request:
            req_json = request["json"]
            if isinstance(req_json, Text):
                req_json = f'"{req_json}"'
            step_info.with_json(req_json)

        if "timeout" in request:
            timeout = request["timeout"]
            step_info.set_timeout(timeout)

        if "verify" in request:
            verify = request["verify"]
            step_info.set_verify(verify)

        if "allow_redirects" in request:
            allow_redirects = request["allow_redirects"]
            step_info.set_allow_redirects(allow_redirects)

        if "upload" in request:
            upload = request["upload"]
            step_info.upload(**upload)

        return step_info

    def _init_teststeps(self):
        teststeps = self.__case_info.get('teststeps', None)
        if not teststeps:
            raise exceptions.ParamsError('-----lack teststeps------')
        step_list = []
        for teststep in teststeps:
            step_info = self._init_teststep(teststep)
            step_list.append(step_info)
        self.teststeps = step_list

    def _init_teststep(self, teststep: Dict) -> Step:
        """
        init teststeps
        :return:
        """
        if not teststep:
            raise exceptions.ParamsError('-----lack teststep------')
        if teststep.get("request"):
            step_info = RunRequest(teststep["name"])
        elif teststep.get("testcase"):
            step_info = RunTestCase(teststep["name"])
        else:
            raise exceptions.TestCaseFormatError(f"Invalid teststep: {teststep}")

        if "variables" in teststep:
            variables = teststep["variables"]
            step_info.with_variables(**variables)

        if "setup_hooks" in teststep:
            setup_hooks = teststep["setup_hooks"]
            for hook in setup_hooks:
                if isinstance(hook, Text):
                    step_info.setup_hook(hook)
                elif isinstance(hook, Dict) and len(hook) == 1:
                    assign_var_name, hook_content = list(hook.items())[0]
                    step_info.setup_hook(hook_content, assign_var_name)
                else:
                    raise exceptions.TestCaseFormatError(f"Invalid setup hook: {hook}")

        if teststep.get("request"):
            request = teststep.get("request")
            url = request["url"]
            method = request["method"].lower()
            if hasattr(step_info, method):
                step_info = getattr(step_info, method)(url)
                step_info = self._init_request(request, step_info)
        elif teststep.get("testcase"):
            testcase = teststep["testcase"]
            step_info.call(testcase)
            # call_ref_testcase = f".call({testcase})"
            # step_info += call_ref_testcase

        if "teardown_hooks" in teststep:
            teardown_hooks = teststep["teardown_hooks"]
            for hook in teardown_hooks:
                if isinstance(hook, Text):
                    step_info.teardown_hook(hook)
                elif isinstance(hook, Dict) and len(hook) == 1:
                    assign_var_name, hook_content = list(hook.items())[0]
                    step_info.teardown_hook(hook_content, assign_var_name)
                else:
                    raise exceptions.TestCaseFormatError(f"Invalid teardown hook: {hook}")

        if "extract" in teststep:
            # request step
            step_info = step_info.extract()
            for extract_name, extract_path in teststep["extract"].items():
                step_info.with_jmespath(extract_path, extract_name)

        if "export" in teststep:
            # reference testcase step
            export: List[Text] = teststep["export"]
            step_info += f".export(*{export})"

        if "validate" in teststep:
            step_info = step_info.validate()

            for v in teststep["validate"]:
                validator = uniform_validator(v)
                assert_method = validator["assert"]
                check = validator["check"]
                # if '"' in check:
                # e.g. body."user-agent" => 'body."user-agent"'
                # check = f"'{check}'"
                # else:
                #     check = f'"{check}"'
                expect = validator["expect"]
                # if isinstance(expect, Text):
                #     expect = f'"{expect}"'

                message = validator["message"]
                assert_method_str = f"assert_{assert_method}"
                if message:
                    step_info = getattr(step_info, assert_method_str)(check, expect, message)
                    # step_info += f".assert_{assert_method}({check}, {expect}, '{message}')"
                else:
                    step_info = getattr(step_info, assert_method_str)(check, expect)
        step = Step(step_info)
        return step


class TestCaseMate:
    def __init__(self):
        self.project_meta = None
        self.pytest_files_made_cache_mapping = {}
        self.pytest_files_run_set = set()
        self.tests_paths = []

    def main_make(self, tests_paths: List[Text]) -> List[Set]:
        self.tests_paths = tests_paths
        # 初始化项目
        for tests_path in self.tests_paths:
            tests_path = ensure_path_sep(tests_path)
            if not os.path.isabs(tests_path):
                tests_path = os.path.join(os.getcwd(), tests_path)

            self.__make(tests_path)

        return list(self.pytest_files_run_set)

    def __make(self, tests_path: Text):
        """ make testcase(s) with testcase/testsuite/folder absolute path
            generated pytest file path will be cached in pytest_files_made_cache_mapping

        Args:
            tests_path: should be in absolute path

        """
        logger.info(f"make path: {tests_path}")
        test_files = []
        if os.path.isdir(tests_path):
            files_list = load_folder_files(tests_path)
            test_files.extend(files_list)
        elif os.path.isfile(tests_path):
            test_files.append(tests_path)
        else:
            raise exceptions.TestcaseNotFound(f"Invalid tests path: {tests_path}")

        for test_file in test_files:
            if test_file.lower().endswith("_test.py"):
                self.pytest_files_run_set.add(test_file)
                continue

            try:
                test_content = load_test_file(test_file)
            except (exceptions.FileNotFound, exceptions.FileFormatError) as ex:
                logger.warning(f"Invalid test file: {test_file}\n{type(ex).__name__}: {ex}")
                continue

            if not isinstance(test_content, Dict):
                logger.warning(
                    f"Invalid test file: {test_file}\n"
                    f"reason: test content not in dict format."
                )
                continue

            # api in v2 format, convert to v3 testcase
            if "request" in test_content and "name" in test_content:
                test_content = ensure_testcase_v3_api(test_content)

            if "config" not in test_content:
                logger.warning(
                    f"Invalid testcase/testsuite file: {test_file}\n"
                    f"reason: missing config part."
                )
                continue
            elif not isinstance(test_content["config"], Dict):
                logger.warning(
                    f"Invalid testcase/testsuite file: {test_file}\n"
                    f"reason: config should be dict type, got {test_content['config']}"
                )
                continue

            # ensure path absolute
            test_content.setdefault("config", {})["path"] = test_file

            # testcase
            if "teststeps" in test_content:
                try:
                    testcase_pytest_path = self.make_testcase(test_content, tests_path=tests_path)
                    self.pytest_files_run_set.add(testcase_pytest_path)
                except exceptions.TestCaseFormatError as ex:
                    logger.warning(
                        f"Invalid testcase file: {test_file}\n{type(ex).__name__}: {ex}"
                    )
                    continue

            # testsuite
            # elif "testcases" in test_content:
            #     try:
            #         make_testsuite(test_content)
            #     except exceptions.TestSuiteFormatError as ex:
            #         logger.warning(
            #             f"Invalid testsuite file: {test_file}\n{type(ex).__name__}: {ex}"
            #         )
            #         continue

            # invalid format
            else:
                logger.warning(
                    f"Invalid test file: {test_file}\n"
                    f"reason: file content is neither testcase nor testsuite"
                )

    def make_testcase(self, testcase: Dict, dir_path: Text = None, tests_path: Text = None) -> Text:
        """convert valid testcase dict to pytest file path"""
        # ensure compatibility with testcase format v2
        testcase = ensure_testcase_v3(testcase)

        # validate testcase format
        load_testcase(testcase)
        testcase_abs_path = self.__ensure_absolute(testcase["config"]["path"])
        logger.info(f"start to make testcase: {testcase_abs_path}")

        testcase_python_abs_path, testcase_cls_name = self.convert_testcase_path(
            testcase_abs_path
        )
        if dir_path:
            testcase_python_abs_path = os.path.join(
                dir_path, os.path.basename(testcase_python_abs_path)
            )

        if testcase_python_abs_path in self.pytest_files_made_cache_mapping:
            return testcase_python_abs_path

        config = testcase["config"]
        config["path"] = self.convert_relative_project_root_dir(testcase_python_abs_path)
        config["variables"] = self.convert_variables(config.get("variables", {}))

        # prepare reference testcase
        imports_list = []
        teststeps = testcase["teststeps"]
        for teststep in teststeps:
            if not teststep.get("testcase"):
                continue

            # make ref testcase pytest file
            ref_testcase_path = self.__ensure_absolute(teststep["testcase"])
            test_content = load_test_file(ref_testcase_path)

            if not isinstance(test_content, Dict):
                raise exceptions.TestCaseFormatError(f"Invalid teststep: {teststep}")

            # api in v2 format, convert to v3 testcase
            if "request" in test_content and "name" in test_content:
                test_content = ensure_testcase_v3_api(test_content)

            test_content.setdefault("config", {})["path"] = ref_testcase_path
            ref_testcase_python_abs_path = self.make_testcase(test_content)

            # override testcase export
            ref_testcase_export: List = test_content["config"].get("export", [])
            if ref_testcase_export:
                step_export: List = teststep.setdefault("export", [])
                step_export.extend(ref_testcase_export)
                teststep["export"] = list(set(step_export))

            # prepare ref testcase class name
            ref_testcase_cls_name = self.pytest_files_made_cache_mapping[
                ref_testcase_python_abs_path
            ]
            teststep["testcase"] = ref_testcase_cls_name

            # prepare import ref testcase
            ref_testcase_python_relative_path = self.convert_relative_project_root_dir(
                ref_testcase_python_abs_path
            )
            ref_module_name, _ = os.path.splitext(ref_testcase_python_relative_path)
            ref_module_name = ref_module_name.replace(os.sep, ".")
            import_expr = f"from {ref_module_name} import TestCase{ref_testcase_cls_name} as {ref_testcase_cls_name}"
            if import_expr not in imports_list:
                imports_list.append(import_expr)

        testcase_path = self.convert_relative_project_root_dir(testcase_abs_path)
        # current file compared to ProjectRootDir
        diff_levels = len(testcase_path.split(os.sep))

        data = {
            "version": __version__,
            "testcase_path": testcase_path,
            "diff_levels": diff_levels,
            "project_path": f'{tests_path}',
            "class_name": f"TestCase{testcase_cls_name}",
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

        self.pytest_files_made_cache_mapping[testcase_python_abs_path] = testcase_cls_name
        _ensure_testcase_module(testcase_python_abs_path)

        logger.info(f"generated testcase: {testcase_python_abs_path}")

        return testcase_python_abs_path

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

    def convert_testcase_path(self, testcase_abs_path: Text) -> Tuple[Text, Text]:
        """convert single YAML/JSON testcase path to python file"""
        testcase_new_path = self.ensure_file_abs_path_valid(testcase_abs_path)

        dir_path = os.path.dirname(testcase_new_path)
        file_name, _ = os.path.splitext(os.path.basename(testcase_new_path))
        testcase_python_abs_path = os.path.join(dir_path, f"{file_name}_test.py")

        # convert title case, e.g. request_with_variables => RequestWithVariables
        name_in_title_case = file_name.title().replace("_", "")

        return testcase_python_abs_path, name_in_title_case

    def __ensure_absolute(self, path: Text) -> Text:
        if path.startswith("./"):
            # Linux/Darwin, hrun ./test.yml
            path = path[len("./"):]
        elif path.startswith(".\\"):
            # Windows, hrun .\\test.yml
            path = path[len(".\\"):]

        path = ensure_path_sep(path)
        self.load_project_meta(path)

        if os.path.isabs(path):
            absolute_path = path
        else:
            absolute_path = os.path.join(self.project_meta.RootDir, path)

        if not os.path.isfile(absolute_path):
            logger.error(f"Invalid testcase file path: {absolute_path}")
            raise exceptions.FileNotFound(f"Invalid testcase file path: {absolute_path}")

        return absolute_path

    def ensure_file_abs_path_valid(self, file_abs_path: Text) -> Text:
        """ ensure file path valid for pytest, handle cases when directory name includes dot/hyphen/space

        Args:
            file_abs_path: absolute file path

        Returns:
            ensured valid absolute file path

        """
        raw_abs_file_name, file_suffix = os.path.splitext(file_abs_path)
        file_suffix = file_suffix.lower()

        raw_file_relative_name = self.convert_relative_project_root_dir(raw_abs_file_name)
        if raw_file_relative_name == "":
            return file_abs_path

        path_names = []
        for name in raw_file_relative_name.rstrip(os.sep).split(os.sep):

            if name[0] in string.digits:
                # ensure file name not startswith digit
                # 19 => T19, 2C => T2C
                name = f"T{name}"

            if name.startswith("."):
                # avoid ".csv" been converted to "_csv"
                pass
            else:
                # handle cases when directory name includes dot/hyphen/space
                name = name.replace(" ", "_").replace(".", "_").replace("-", "_")

            path_names.append(name)

        new_file_path = os.path.join(
            self.project_meta.RootDir, f"{os.sep.join(path_names)}{file_suffix}"
        )
        return new_file_path

    def convert_relative_project_root_dir(self, abs_path: Text) -> Text:
        """ convert absolute path to relative path, based on project_meta.RootDir

        Args:
            abs_path: absolute path

        Returns: relative path based on project_meta.RootDir

        """
        if not abs_path.startswith(self.project_meta.RootDir):
            raise exceptions.ParamsError(
                f"failed to convert absolute path to relative path based on project_meta.RootDir\n"
                f"abs_path: {abs_path}\n"
                f"project_meta.RootDir: {self.project_meta.RootDir}"
            )

        return abs_path[len(self.project_meta.RootDir) + 1:]

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

    def __del__(self):
        if self.project_meta.RootDir in sys.path:
            sys.path.remove(self.project_meta.RootDir)
