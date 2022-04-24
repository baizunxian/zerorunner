import os
import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException

from autotest.utils.ui.web.config import element_wait_timeout, page_flash_timeout
from autotest.utils.ui.web.locator import locating


def now():
    t = time.time()
    return time.strftime("@%Y%m%d_%H%M%S", time.localtime(t))


def timestamp():
    # js 格式的时间戳
    return int(time.time() * 1000)


class Driver:
    def __init__(self):
        self.start_time = now()
        self.start_timestamp = timestamp()
        self.plan_name = ''
        self.sheet_name = ''
        self.plan_data = {}
        self.testsuite_data = {}
        self.no = 1
        self.driver = ''
        self.snippet = {}
        self.caseset = {}
        self.executable_path = 'D:\\project\\auto_test\\autotest_backend\\autotest\\utils\\ui\\chromedriver.exe'
        self.command_executor = 'http://10.83.32.33:4444/wd/hub'
        self.driver = self.set_driver()

    def init(self, desired_caps, server_url):
        self.desired_caps = desired_caps
        self.server_url = server_url
        self.platform = desired_caps.get('platformName', 'desktop')
        self.browserName = desired_caps.get('browserName', 'chrome')
        self.headless = desired_caps.pop('headless', False)
        self.snapshot = desired_caps.pop('snapshot', False)
        self.executable_path = 'D:\\project\\auto_test\\autotest_backend\\autotest\\utils\\ui\\chromedriver.exe'
        # self.executable_path = desired_caps.pop('executable_path', False)

    def set_driver(self):
        self.test_data = {'_last_': False}
        self.var = {}
        self.caseset = {}
        self.casesets = []  # 用例组合执行容器
        # self.current_page = '通用'
        # self.db = {}
        # self.http = {}
        # self.windows = {}
        # self.baseurl = {}
        # self.action = {}
        # self.wait_times = 0

        # if self.platform.lower() == 'desktop':
        #     if self.browserName.lower() == 'ie':
        #         # capabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER
        #         # capabilities['acceptInsecureCerts'] = True
        #         if self.executable_path:
        #             self.driver = webdriver.Ie(executable_path=self.executable_path)
        #         else:
        #             self.driver = webdriver.Ie()
        #     elif self.browserName.lower() == 'firefox':
        #         profile = webdriver.FirefoxProfile()
        #         profile.accept_untrusted_certs = True
        #
        #         options = webdriver.FirefoxOptions()
        #         # 如果配置了 headless 模式
        #         if self.headless:
        #             # options.set_headless()
        #             # options.add_argument('-headless')
        #             options.add_argument('--disable-gpu')
        #             options.add_argument("--no-sandbox")
        #             options.add_argument('window-size=1920x1080')
        #
        #         if self.executable_path:
        #             self.driver = webdriver.Firefox(
        #                 firefox_profile=profile, firefox_options=options, executable_path=self.executable_path)
        #         else:
        #             self.driver = webdriver.Firefox(
        #                 firefox_profile=profile, firefox_options=options)
        #         self.driver.maximize_window()
        #     elif self.browserName.lower() == 'chrome':
        options = webdriver.ChromeOptions()

        # 如果配置了 headless 模式
        # if self.headless:
        #     options.add_argument('--headless')
        #     options.add_argument('--disable-gpu')
        #     options.add_argument("--no-sandbox")
        #     options.add_argument('window-size=1920x1080')

        # options.add_argument("--start-maximized")
        # options.add_argument('--ignore-certificate-errors')
        # 指定浏览器分辨率，当"--start-maximized"无效时使用
        # options.add_argument('window-size=1920x1080')
        # prefs = {}
        # prefs["credentials_enable_service"] = False
        # prefs["profile.password_manager_enabled"] = False
        # options.add_experimental_option("prefs", prefs)
        # options.add_argument('disable-infobars')
        # options.add_experimental_option("excludeSwitches", ['load-extension', 'enable-automation'])
        #
        chrome_driver = os.path.abspath(r"/data/project/selenium/chromedriver")
        os.environ["webdriver.chrome.driver"] = chrome_driver
        chrome_capabilities = {
            "browserName": "chrome",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True,
            "webdriver.chrome.driver": chrome_driver
        }

        # if self.executable_path:
        # driver = webdriver.Chrome(options=options, executable_path=self.executable_path)
        # else:
        driver = webdriver.Remote(command_executor=self.command_executor, options=options,
                                  desired_capabilities=chrome_capabilities)

        # 等待元素超时时间
        driver.implicitly_wait(element_wait_timeout)  # seconds
        # 页面刷新超时时间
        driver.set_page_load_timeout(page_flash_timeout)  # seconds
        driver.maximize_window()

        return driver
        # else:
        #     raise Exception(
        #         'Error: this browser is not supported or mistake name：%s' % self.browserName)

        # elif self.platform.lower() == 'ios':
        #     from appium import webdriver as appdriver
        #     if not self.driver:
        #         self.driver = appdriver.Remote(self.server_url, self.desired_caps)
        #
        # elif self.platform.lower() == 'android':
        #     from appium import webdriver as appdriver
        #     if not self.driver:
        #         self.driver = appdriver.Remote(self.server_url, self.desired_caps)
        #
        # elif self.platform.lower() == 'windows':
        #     from pywinauto.application import Application
        #     from sweetest.keywords.windows import Windows
        #     self.desired_caps.pop('platformName')
        #     backend = self.desired_caps.pop('backend', 'win32')
        #     _path = ''
        #     if self.desired_caps.get('#path'):
        #         _path = self.desired_caps.pop('#path')
        #         _backend = self.desired_caps.pop('#backend')
        #
        #     if self.desired_caps.get('cmd_line'):
        #         app = Application(backend).start(**self.desired_caps)
        #     elif self.desired_caps.get('path'):
        #         app = Application(backend).connect(**self.desired_caps)
        #     else:
        #         raise Exception('Error: Windows GUI start/connect args error')
        #     self.windows['default'] = Windows(app)
        #
        #     if _path:
        #         _app = Application(_backend).connect(path=_path)
        #         self.windows['#'] = Windows(_app)

    def plan_end(self):
        self.plan_data['plan'] = self.plan_name
        # self.plan_data['task'] = self.start_timestamp
        self.plan_data['start_timestamp'] = self.start_timestamp
        self.plan_data['end_timestamp'] = int(time.time() * 1000)

        return self.plan_data

    def open(self, step):
        self.driver.get(step['data'])
        # self.driver.get_screenshot_as_file("baidu_img.png")
        time.sleep(0.5)

    def input(self, step):
        data = step['data']
        element = step['element']
        element_location = locating(element, self.driver)

        # if step['data'].get('清除文本', '') == '否' or step['data'].get('clear', '').lower() == 'no':
        #     pass
        # else:
        #     element_location.clear()

        # for key in data:
        #     if key.startswith('text'):
        #         if isinstance(data[key], tuple):
        #             element_location.send_keys(*data[key])
        #         elif element_location:
        #             element_location.send_keys(data[key])
        #         time.sleep(0.5)
        #     if key == 'word':  # 逐字输入
        #         for d in data[key]:
        #             element_location.send_keys(d)
        #             time.sleep(0.3)
        element_location.send_keys(data)
        # self.driver.get_screenshot_as_file("baidu_img1.png")
        return element_location

    def switch_to_frame(self, step):
        data = step['data']
        element = step['element']
        element_location = locating(element, self.driver, 'XPATH')
        self.driver.implicitly_wait(10)
        self.driver.switch_to.frame(element_location)
        # icon_QRcode = self.driver.find_element_by_xpath('//*[@id="scan_login-wrap"]/div[1]/img')
        # print(icon_QRcode.text)
        # icon_QRcode.click()

    def click(self, step):
        element = step['element']
        data = step['data']
        if isinstance(element, dict):
            element_location = locating(element, self.driver, 'CLICK')
            if element_location:
                try:
                    element_location.click()
                except ElementClickInterceptedException:  # 如果元素为不可点击状态，则等待1秒，再重试一次
                    time.sleep(1)
                    if data.get('mode'):
                        self.driver.execute_script("arguments[0].click();", element_location)
                    else:
                        element_location.click()
        elif isinstance(element, list):
            for _e in element:
                element_location = locating(_e, 'CLICK')
                try:
                    element_location.click()
                except ElementClickInterceptedException:  # 如果元素为不可点击状态，则等待1秒，再重试一次
                    time.sleep(1)
                    if data.get('mode'):
                        g.driver.execute_script("arguments[0].click();", element_location)
                    else:
                        element_location.click()
                time.sleep(0.5)
        time.sleep(0.5)

        # 获取元素其他属性
        output = step['output']
        for key in output:
            if output[key] == 'text':
                g.var[key] = element_location.text
            elif output[key] in ('text…', 'text...'):
                if element_location.text.endswith('...'):
                    g.var[key] = element_location.text[:-3]
                else:
                    g.var[key] = element_location.text
            else:
                g.var[key] = element_location.get_attribute(output[key])

        # 判断是否打开了新的窗口，并将新窗口添加到所有窗口列表里
        # all_handles = g.driver.window_handles
        # for handle in all_handles:
        #     if handle not in w.windows.values():
        #         w.register(step, handle)

        return element_location


if __name__ == '__main__':
    print(getattr(Driver, 'plan_end'))
