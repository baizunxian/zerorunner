import re
from time import sleep

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from zerorunner.models.step_model import TUiRequest
from zerorunner.ext.zero_driver.driver import ZeroDriver
from zerorunner.ext.zero_driver.locator import locating


class Common:
    @staticmethod
    def title(zero_driver: ZeroDriver):
        """获取页面标题"""
        return zero_driver.driver.title

    @staticmethod
    def current_url(zero_driver: ZeroDriver):
        """获取当前页面的url"""
        return zero_driver.driver.current_url


class WebAction:
    """web动作"""
    @staticmethod
    def open(zero_driver: ZeroDriver, step: TUiRequest):
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
        zero_driver.driver.get(step.data)
        if step.cookie:
            zero_driver.driver.add_cookie(step.cookie)
        sleep(0.5)

    @staticmethod
    def check(step: TUiRequest, zero_driver: ZeroDriver):
        """检查元素"""
        element_location = locating(zero_driver, step)
        output = step.output
        var = {}

        if step.location_method in ('title', 'current_url'):
            var[step.location_method] = getattr(Common, step.location_method)(step.location_value, output)

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
    def input(zero_driver: ZeroDriver, step: TUiRequest):
        element_location = locating(zero_driver, step)
        element_location.clear()
        element_location.send_keys(step.data)
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
    def switch_to_frame(zero_driver: ZeroDriver, step: TUiRequest):
        element_location = locating(zero_driver, step)
        zero_driver.driver.implicitly_wait(10)
        zero_driver.driver.switch_to.frame(element_location)
        # icon_QRcode = self.driver.find_element_by_xpath('//*[@id="scan_login-wrap"]/div[1]/img')
        # print(icon_QRcode.text)
        # icon_QRcode.click()

    @staticmethod
    def click(zero_driver: ZeroDriver, step: TUiRequest):
        element_location = locating(zero_driver, step)
        if element_location:
            try:
                element_location.click()
            except ElementClickInterceptedException:  # 如果元素为不可点击状态，则等待1秒，再重试一次
                sleep(1)
                # if data.get('mode'):
                #     zero_driver.driver.execute_script("arguments[0].click();", element_location)
                # else:
                element_location.click()

        sleep(0.5)

        # 获取元素其他属性
        # zero_driver._session_var[key] = element_location.get_attribute(output[key])

        # 判断是否打开了新的窗口，并将新窗口添加到所有窗口列表里
        # all_handles = zero_driver.driver.window_handles
        # for handle in all_handles:
        #     if handle not in w.windows.values():
        #         w.register(step, handle)

        return element_location

    @staticmethod
    def select(zero_driver: ZeroDriver, step: TUiRequest):
        """选择"""
        element_location = locating(zero_driver, step)
        for key in data:
            if key.startswith('index'):
                Select(element_location).select_by_index(data[key])
            elif key.startswith('value'):
                Select(element_location).select_by_value(data[key])
            elif key.startswith('text') or key.startswith('visible_text'):
                Select(element_location).select_by_visible_text(data[key])

    @staticmethod
    def deselect(zero_driver: ZeroDriver, step: TUiRequest):
        """取消选择"""
        element_location = locating(zero_driver, step)
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
    def hover(zero_driver: ZeroDriver, step: TUiRequest):
        actions = ActionChains(zero_driver.driver)
        element_location = locating(zero_driver, step)
        actions.move_to_element(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def context_click(zero_driver: ZeroDriver, step: TUiRequest):
        actions = ActionChains(zero_driver.driver)
        element_location = locating(zero_driver, step)
        actions.context_click(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def double_click(zero_driver: ZeroDriver, step: TUiRequest):
        actions = ActionChains(zero_driver.driver)
        element_location = locating(zero_driver, step)
        actions.double_click(element_location)
        actions.perform()
        sleep(0.5)

        return element_location

    @staticmethod
    def drag_and_drop(zero_driver: ZeroDriver, step: TUiRequest):
        """拖拽"""
        actions = ActionChains(zero_driver.driver)
        source = locating(element[0])
        target = locating(element[1])
        actions.drag_and_drop(source, target)
        actions.perform()
        sleep(0.5)

    @staticmethod
    def swipe(zero_driver: ZeroDriver, step: TUiRequest):
        """滑动"""
        actions = ActionChains(zero_driver.driver)
        source = locating(zero_driver, step)
        x = data.get('x', 0)
        y = data.get('y', 0)
        actions.drag_and_drop_by_offset(source, x, y)
        actions.perform()
        sleep(0.5)

    @staticmethod
    def script(zero_driver: ZeroDriver, step: TUiRequest):
        """执行脚本"""
        zero_driver.driver.execute_script(step.location_value)

    @staticmethod
    def message(zero_driver: ZeroDriver, step: TUiRequest):
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
    def upload(zero_driver: ZeroDriver, step: TUiRequest):
        """上传文件"""
        import win32com.client

        data = step['data']
        element = step['element']
        element_location = locating(zero_driver, step)
        file_path = data.get('text', '') or data.get('file', '')

        element_location.click()
        sleep(3)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Sendkeys(file_path)
        sleep(2)
        shell.Sendkeys("{ENTER}")
        sleep(2)

    @staticmethod
    def navigate(zero_driver: ZeroDriver, step: TUiRequest):
        """导航"""
        if step.location_value.lower() in ('刷新', 'refresh'):
            zero_driver.driver.refresh()
        elif step.location_value.lower() in ('前进', 'forward'):
            zero_driver.driver.forward()
        elif step.location_value.lower() in ('后退', 'back'):
            zero_driver.driver.back()

    @staticmethod
    def scroll(zero_driver: ZeroDriver, step: TUiRequest):
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
                zero_driver.driver.execute_script(f"document.documentElement.scrollTop={y}")
            if x:
                zero_driver.driver.execute_script(f"document.documentElement.scrollLeft={x}")
        else:
            element_location = locating(zero_driver, step)

            if y:
                zero_driver.driver.execute_script(f"arguments[0].scrollTop={y}", element_location)
            if x:
                zero_driver.driver.execute_script(f"arguments[0].scrollLeft={x}", element_location)
