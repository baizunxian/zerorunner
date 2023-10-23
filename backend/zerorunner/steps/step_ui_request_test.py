# -*- coding: utf-8 -*-
# @author: xiaobai
from zerorunner.models.step_model import TStep, TUiRequest, TConfig
from zerorunner.runner import SessionRunner
from zerorunner.steps.step import Step
from zerorunner.steps.step_ui_requet import RunUiStep
from zerorunner.ext.zero_driver.driver import DriverSetting, ZeroDriver

if __name__ == '__main__':
    runner = SessionRunner()
    runner.config = TConfig(
        name="test",
    )

    step1 = TStep(
        name="test",
        step_type="ui",
        ui_request=TUiRequest(
            action="open",
            data="https://www.baidu.com"
        )
    )
    step2 = TStep(
        name="test2",
        step_type="ui",
        ui_request=TUiRequest(
            action="input",
            location_method="xpath",
            location_value="//input[@id='kw']",
            data="哈哈哈11211",
        )
    )
    step_list = [Step(RunUiStep(step1)), Step(RunUiStep(step2))]

    driver_setting = DriverSetting(
        command_executor="http://xiaobaicodes.com:4444/wd/hub",
        headless=False
    )
    driver_app = ZeroDriver(driver_setting)
    runner.driver_app = driver_app
    for step in step_list:
        runner.run_step(step)
    driver_app.get_screenshot('file', "test.png")
    driver_app.driver.quit()
