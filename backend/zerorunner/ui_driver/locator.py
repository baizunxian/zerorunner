from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from zerorunner.model.step_model import TUiRequest
from zerorunner.ui_driver.driver import DriverApp


def locating(driver_app: DriverApp, step: TUiRequest):
    """定位元素"""
    wait = WebDriverWait(driver_app.driver, driver_app.setting.element_wait_timeout)
    if step.location_type in ('title', 'url', 'current_url'):
        return None
    else:
        try:
            location = wait.until(EC.presence_of_element_located(
                (getattr(By, step.location_type.upper()), step.location_value)))
        except:
            sleep(5)
            try:
                location = wait.until(EC.presence_of_element_located(
                    (getattr(By, step.location_type.upper()), step.location_value)))
            except:
                raise Exception(f'定位元素:{step.location_value} 失败: 超时')
    try:
        if driver_app.driver.name in ('chrome', 'safari'):
            driver_app.driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true)", location)
        else:
            driver_app.driver.execute_script("arguments[0].scrollIntoView(false)", location)
    except:
        pass

    try:
        if step.action.upper() == 'CLICK':
            location = wait.until(EC.element_to_be_clickable(
                (getattr(By, step.location_type.upper()), step.location_value)))
        else:
            location = wait.until(EC.visibility_of_element_located(
                (getattr(By, step.location_type.upper()), step.location_value)))
    except:
        pass

    return location
