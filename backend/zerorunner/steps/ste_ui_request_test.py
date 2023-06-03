# -*- coding: utf-8 -*-
# @author: xiaobai
from zerorunner.model.step_model import TStep, TUiRequest
from zerorunner.models import TConfig
from zerorunner.runner_new import SessionRunner
from zerorunner.steps.step import Step
from zerorunner.steps.step_ui_requet import RunUiStep
from zerorunner.ui_driver.driver import DriverSetting, DriverApp

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
            input_data="https://www.baidu.com"
        )
    )
    step2 = TStep(
        name="test2",
        step_type="ui",
        ui_request=TUiRequest(
            action="input",
            location_type="xpath",
            location_value="//input[@id='kw']",
            input_data="哈哈哈",
        )
    )
    step_list = [Step(RunUiStep(step1)), Step(RunUiStep(step2))]

    driver_setting = DriverSetting(
        command_executor="http://xiaobaicodes.com:4444/wd/hub",
        headless=False
    )
    driver_app = DriverApp(driver_setting)
    runner.driver_app = driver_app
    for step in step_list:
        runner.run_step(step)
    driver_app.get_screenshot('file', "test.png")
    driver_app.driver.quit()
