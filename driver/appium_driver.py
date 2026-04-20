import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options


def get_connected_device():
    """연결된 Android 기기의 UDID를 자동으로 가져옴"""
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")[1:]  # 첫 줄(헤더) 제외
    devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]

    if not devices:
        raise RuntimeError("연결된 Android 기기가 없습니다. USB 연결을 확인하세요.")

    return devices[0]


def create_android_driver(
    server_url: str = "http://localhost:4723",
):
    device_udid = get_connected_device()

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    options.device_name = device_udid
    options.udid = device_udid

    options.no_reset = True
    options.dont_stop_app_on_reset = True

    options.new_command_timeout = 300

    driver = webdriver.Remote(
        command_executor=server_url,
        options=options
    )

    return driver
