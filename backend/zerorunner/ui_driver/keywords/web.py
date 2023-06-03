import re
from time import sleep

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from zerorunner.model.step_model import TUiRequest
from zerorunner.ui_driver.driver import DriverApp
from zerorunner.ui_driver.locator import locating


class Common:
    @staticmethod
    def title(driver_app: DriverApp):
        """获取页面标题"""
        return driver_app.driver.title

    @staticmethod
    def current_url(driver_app: DriverApp):
        """获取当前页面的url"""
        return driver_app.driver.current_url


class WebAction:
    """web动作"""
    @staticmethod
    def open(driver_app: DriverApp, step: TUiRequest):
        # if step['data'].get('清理缓存', '') or step['data'].get('clear', ''):
        #     g.driver.delete_all_cookies()
        # if step['data'].get('#open_type', '') in ('新标签页', 'tab'):
        #     js = "window.open('%s')" % value
        #     g.driver.execute_script(js)
        # 判断是否打开了新的窗口，并将新窗口添加到所有窗口列表里
        # all_handles = g.driver.window_handles
        # for handle in all_handles:
        #     if handle not in w.windows.values():
        #         w.register(step, handle)
        # else:
        # if step['data'].get('#open_type', '') in ('新浏览器', 'browser'):
        #     w.close()
        #     g.set_driver()
        #     w.init()
        driver_app.driver.get(step.input_data)
        if step.cookie:
            driver_app.driver.add_cookie(step.cookie)
        sleep(0.5)

    @staticmethod
    def check(step: TUiRequest, driver_app: DriverApp):
        """检查元素"""
        element_location = locating(driver_app, step)
        output = step.output
        var = {}

        if step.location_type in ('title', 'current_url'):
            var[step.location_type] = getattr(Common, step.location_type)(step.location_value, output)

        else:
            for key in data:
                # 预期结果
                expected = data[key]
                # 切片操作处理
                s = re.findall(r'\[.*?\]', key)
                if s:
                    s = s[0]
                    key = key.replace(s, '')

                if key == 'text':
                    real = element_location.text
                else:
                    real = element_location.get_attribute(key)
                if s:
                    real = eval('real' + s)

                logger.info('DATA:%s' % repr(expected))
                logger.info('REAL:%s' % repr(real))
                try:
                    compare(expected, real)
                except:
                    raise Exception(f'Check Failure, DATA:{repr(expected)}, REAL:{repr(real)}')

            # 获取元素其他属性
            for key in output:
                if output[key] == 'text':
                    var[key] = g.var[key] = element_location.text
                elif output[key] in ('text…', 'text...'):
                    if element_location.text.endswith('...'):
                        var[key] = g.var[key] = element_location.text[:-3]
                    else:
                        var[key] = g.var[key] = element_location.text
                else:
                    var[key] = g.var[key] = element_location.get_attribute(output[key])
        if var:
            step['_output'] += '\n||output=' + str(var)
        return element_location

    @staticmethod
    def notcheck(step):
        data = step['data']
        if not data:
            data = step['expected']

        element = step['element']
        # element_location = locating_element(element)

        if element['by'] == 'title':
            assert data['text'] != g.driver.title

    @staticmethod
    def input(driver_app: DriverApp, step: TUiRequest):
        element_location = locating(driver_app, step)
        element_location.clear()
        element_location.send_keys(step.input_data)
        # for key in data:
        #     if key.startswith('text'):
        #         if isinstance(data[key], tuple):
        #             element_location.send_keys(*data[key])
        #         elif element_location:
        #             element_location.send_keys(data[key])
        #         sleep(0.5)
        #     if key == 'word':  # 逐字输入
        #         for d in data[key]:
        #             element_location.send_keys(d)
        #             sleep(0.3)
        return element_location

    @staticmethod
    def switch_to_frame(driver_app: DriverApp, step: TUiRequest):
        element_location = locating(driver_app, step)
        driver_app.driver.implicitly_wait(10)
        driver_app.driver.switch_to.frame(element_location)
        # icon_QRcode = self.driver.find_element_by_xpath('//*[@id="scan_login-wrap"]/div[1]/img')
        # print(icon_QRcode.text)
        # icon_QRcode.click()

    @staticmethod
    def click(driver_app: DriverApp, step: TUiRequest):
        element_location = locating(driver_app, step)
        if element_location:
            try:
                element_location.click()
            except ElementClickInterceptedException:  # 如果元素为不可点击状态，则等待1秒，再重试一次
                sleep(1)
                # if data.get('mode'):
                #     driver_app.driver.execute_script("arguments[0].click();", element_location)
                # else:
                element_location.click()

        sleep(0.5)

        # 获取元素其他属性
        # driver_app._session_var[key] = element_location.get_attribute(output[key])

        # 判断是否打开了新的窗口，并将新窗口添加到所有窗口列表里
        # all_handles = driver_app.driver.window_handles
        # for handle in all_handles:
        #     if handle not in w.windows.values():
        #         w.register(step, handle)

        return element_location

    @staticmethod
    def select(driver_app: DriverApp, step: TUiRequest):
        """选择"""
        element_location = locating(driver_app, step)
        for key in data:
            if key.startswith('index'):
                Select(element_location).select_by_index(data[key])
            elif key.startswith('value'):
                Select(element_location).select_by_value(data[key])
            elif key.startswith('text') or key.startswith('visible_text'):
                Select(element_location).select_by_visible_text(data[key])

    @staticmethod
    def deselect(driver_app: DriverApp, step: TUiRequest):
        """取消选择"""
        element_location = locating(driver_app, step)
        for key in data:
            if key.startswith('all'):
                Select(element_location).deselect_all()
            elif key.startswith('index'):
                Select(element_location).deselect_by_index(data[key])
            elif key.startswith('value'):
                Select(element_location).deselect_by_value(data[key])
            elif key.startswith('text') or key.startswith('visible_text'):
                Select(element_location).deselect_by_visible_text(data[key])

    @staticmethod
    def hover(driver_app: DriverApp, step: TUiRequest):
        actions = ActionChains(driver_app.driver)
        element_location = locating(driver_app, step)
        actions.move_to_element(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def context_click(driver_app: DriverApp, step: TUiRequest):
        actions = ActionChains(driver_app.driver)
        element_location = locating(driver_app, step)
        actions.context_click(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def double_click(driver_app: DriverApp, step: TUiRequest):
        actions = ActionChains(driver_app.driver)
        element_location = locating(driver_app, step)
        actions.double_click(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def drag_and_drop(driver_app: DriverApp, step: TUiRequest):
        """拖拽"""
        actions = ActionChains(driver_app.driver)
        source = locating(element[0])
        target = locating(element[1])
        actions.drag_and_drop(source, target)
        actions.perform()
        sleep(0.5)

    @staticmethod
    def swipe(driver_app: DriverApp, step: TUiRequest):
        """滑动"""
        actions = ActionChains(driver_app.driver)
        source = locating(driver_app, step)
        x = data.get('x', 0)
        y = data.get('y', 0)
        actions.drag_and_drop_by_offset(source, x, y)
        actions.perform()
        sleep(0.5)

    @staticmethod
    def script(driver_app: DriverApp, step: TUiRequest):
        """执行脚本"""
        driver_app.driver.execute_script(step.location_value)

    @staticmethod
    def message(driver_app: DriverApp, step: TUiRequest):
        data = step['data']
        text = data.get('text', '')
        element = step['element']
        value = e.get(element)[1]

        if value.lower() in ('确认', 'accept'):
            g.driver.switch_to_alert().accept()
        elif value.lower() in ('取消', '关闭', 'cancel', 'close'):
            g.driver.switch_to_alert().dismiss()
        elif value.lower() in ('输入', 'input'):
            g.driver.switch_to_alert().send_keys(text)
            g.driver.switch_to_alert().accept()
        logger.info('--- Switch Frame: Alert')
        w.frame = 'Alert'

    @staticmethod
    def upload(driver_app: DriverApp, step: TUiRequest):
        """上传文件"""
        import win32com.client

        data = step['data']
        element = step['element']
        element_location = locating(driver_app, step)
        file_path = data.get('text', '') or data.get('file', '')

        element_location.click()
        sleep(3)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Sendkeys(file_path)
        sleep(2)
        shell.Sendkeys("{ENTER}")
        sleep(2)

    @staticmethod
    def navigate(driver_app: DriverApp, step: TUiRequest):
        """导航"""
        if step.location_value.lower() in ('刷新', 'refresh'):
            driver_app.driver.refresh()
        elif step.location_value.lower() in ('前进', 'forward'):
            driver_app.driver.forward()
        elif step.location_value.lower() in ('后退', 'back'):
            driver_app.driver.back()

    @staticmethod
    def scroll(driver_app: DriverApp, step: TUiRequest):
        """滚动"""
        x = data.get('x', 0)
        y = data.get('y', 0)

        element = step['element']
        if element == '':
            # if x is None:
            #     x = '0'
            # g.driver.execute_script(
            #     f"window.scrollTo({x},{y})")
            if y:
                driver_app.driver.execute_script(f"document.documentElement.scrollTop={y}")
            if x:
                driver_app.driver.execute_script(f"document.documentElement.scrollLeft={x}")
        else:
            element_location = locating(driver_app, step)

            if y:
                driver_app.driver.execute_script(f"arguments[0].scrollTop={y}", element_location)
            if x:
                driver_app.driver.execute_script(f"arguments[0].scrollLeft={x}", element_location)
