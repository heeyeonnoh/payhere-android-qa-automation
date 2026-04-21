import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.appium_driver import create_android_driver
from flows.product_flow import ProductFlow
from utils.slack_notifier import send_test_results


def close_any_popup(driver):
    """팝업이 있으면 닫기"""
    try:
        confirm = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "확인")
        confirm.click()
        time.sleep(0.5)
    except:
        pass


@pytest.fixture
def driver():
    """테스트 전: 드라이버 생성 / 테스트 후: 드라이버 종료"""
    driver = create_android_driver()
    close_any_popup(driver)
    time.sleep(1)

    yield driver

    driver.quit()


@pytest.fixture
def driver_at_appium_category(driver):
    """appium 카테고리 화면에서 시작하는 fixture"""
    close_any_popup(driver)
    ProductFlow(driver).go_to_appium_category()
    return driver


def pytest_runtest_logreport(report):
    if report.when == "call":
        if not hasattr(pytest, "_qa_results"):
            pytest._qa_results = {"passed": 0, "failed": 0, "error": 0, "failures": [], "start": time.time()}
        if report.passed:
            pytest._qa_results["passed"] += 1
        elif report.failed:
            pytest._qa_results["failed"] += 1
            pytest._qa_results["failures"].append(report.nodeid)
    elif report.when == "setup" and report.failed:
        if not hasattr(pytest, "_qa_results"):
            pytest._qa_results = {"passed": 0, "failed": 0, "error": 0, "failures": [], "start": time.time()}
        pytest._qa_results["error"] += 1
        pytest._qa_results["failures"].append(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    if not hasattr(pytest, "_qa_results"):
        return
    r = pytest._qa_results
    duration = time.time() - r["start"]
    send_test_results(r["passed"], r["failed"], r["error"], duration, r["failures"])
    del pytest._qa_results
