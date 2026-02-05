from appium import webdriver
from appium.options.android import UiAutomator2Options


def create_android_driver(
    server_url: str = "http://localhost:4723",
):
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    options.device_name = "R9TR40N2YQJ"
    options.udid = "R9TR40N2YQJ"

    options.no_reset = True
    options.dont_stop_app_on_reset = True

    options.new_command_timeout = 300

    driver = webdriver.Remote(
        command_executor=server_url,
        options=options
    )

    return driver
