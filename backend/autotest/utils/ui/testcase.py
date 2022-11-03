import os

from autotest.utils.ui.web.app import App
from autotest.utils.ui.globals import timestamp


class TestCase:
    def __init__(self, testcase):
        self.executable_path = os.path.join(os.getcwd(), 'autotest', 'utils', 'ui', 'chromedriver.exe')
        self.testcase = testcase
        self.snippet_steps = {}
        self.app = App({'browserName': 'chrome', 'executable_path': self.executable_path})
        self.error = {}

    def run(self):
        self.testcase['result'] = 'success'
        self.testcase['report'] = ''
        for index, step in enumerate(self.testcase['steps']):
            # 统计开始时间

            step['start_timestamp'] = timestamp()
            step['snapshot'] = {}
            try:
                getattr(self.app, step['keyword'].lower())(step)
                step['result'] = 'success'
            except Exception as err:
                self.error = err
                self.testcase['result'] = 'fail'
                step['result'] = 'fail'
                step['err_info'] = str(err)
            step['end_timestamp'] = timestamp()
            if self.error:
                step['result'] = 'fail'
                break
        self.app.quit()
        steps = []
        i = 0
        for k in self.snippet_steps:
            steps += self.testcase['steps'][i:k] + self.snippet_steps[k]
            i = k
        steps += self.testcase['steps'][i:]
        self.testcase['steps'] = steps
        return self.testcase
