from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from zerorunner.models.step_model import TUiRequest
from zerorunner.ext.zero_driver.driver import ZeroDriver


def locating(zero_driver: ZeroDriver, step: TUiRequest):
    """定位元素"""
    wait = WebDriverWait(zero_driver.driver, zero_driver.setting.element_wait_timeout)
    if step.location_method in ('title', 'url', 'current_url'):
        return None
    else:
        try:
            location = wait.until(EC.presence_of_element_located(
                (getattr(By, step.location_method.upper()), step.location_value)))
        except:
            sleep(5)
            try:
                location = wait.until(EC.presence_of_element_located(
                    (getattr(By, step.location_method.upper()), step.location_value)))
            except:
                raise Exception(f'定位元素:{step.location_value} 失败: 超时')
    try:
        if zero_driver.driver.name in ('chrome', 'safari'):
            zero_driver.driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true)", location)
        else:
            zero_driver.driver.execute_script("arguments[0].scrollIntoView(false)", location)
    except:
        pass

    try:
        if step.action.upper() == 'CLICK':
            location = wait.until(EC.element_to_be_clickable(
                (getattr(By, step.location_method.upper()), step.location_value)))
        else:
            location = wait.until(EC.visibility_of_element_located(
                (getattr(By, step.location_method.upper()), step.location_value)))
    except:
        pass

    return location
