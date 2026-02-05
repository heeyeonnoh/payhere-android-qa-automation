from appium import webdriver
from appium.options.android import UiAutomator2Options


def create_android_driver(
    app_package: str,
    app_activity: str,
    server_url: str = "http://localhost:4723",
    no_reset: bool = True
):

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    options.device_name = "R9TR40N2YQJ"
    options.udid = "R9TR40N2YQJ"

    options.app_package = app_package
    options.app_activity = app_activity

    options.no_reset = no_reset
    options.new_command_timeout = 300

    options.unicode_keyboard = True
    options.reset_keyboard = True

    driver = webdriver.Remote(
        command_executor=server_url,
        options=options
    )

    return driver
