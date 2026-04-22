import pytest
import time
import subprocess
import sys
import os
import shutil
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.appium_driver import create_android_driver
from flows.product_flow import ProductFlow
from utils.slack_notifier import send_test_results

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_pages_url():
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, cwd=REPO_DIR
        )
        url = result.stdout.strip()
        # https://github.com/owner/repo.git → https://owner.github.io/repo/
        url = url.replace("https://github.com/", "").replace(".git", "")
        owner, repo = url.split("/")
        return f"https://{owner}.github.io/{repo}/"
    except Exception:
        return None


def _deploy_allure_report():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        history_store = os.path.join(REPO_DIR, "allure-history")
        allure_tmp = os.path.join(REPO_DIR, "allure-tmp")
        # 저장된 히스토리를 allure-tmp/history에 복사 → 트렌드 반영
        if os.path.exists(history_store):
            history_for_report = os.path.join(allure_tmp, "history")
            if os.path.exists(history_for_report):
                shutil.rmtree(history_for_report)
            shutil.copytree(history_store, history_for_report)
        subprocess.run(
            ["allure", "generate", "allure-tmp", "--clean", "-o", "allure-report"],
            check=True, capture_output=True, cwd=REPO_DIR
        )
        # 새 히스토리를 allure-history에 저장 → 다음 실행에 사용
        new_history = os.path.join(REPO_DIR, "allure-report", "history")
        if os.path.exists(new_history):
            if os.path.exists(history_store):
                shutil.rmtree(history_store)
            shutil.copytree(new_history, history_store)
        # 날짜+시간 폴더에 결과 저장
        archive_dir = os.path.join(REPO_DIR, "allure-results", timestamp)
        shutil.copytree(allure_tmp, archive_dir)
        result = subprocess.run(
            [sys.executable, "-m", "ghp_import", "-n", "-p", "-f", "allure-report"],
            capture_output=True, text=True, cwd=REPO_DIR
        )
        if result.returncode != 0:
            print(f"ghp_import 오류: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, "ghp_import")
        # allure-results/{timestamp} + allure-history를 main 브랜치에 커밋 & 푸시
        subprocess.run(["git", "add", f"allure-results/{timestamp}/", "allure-history/"], cwd=REPO_DIR)
        subprocess.run(
            ["git", "commit", "-m", f"test: Allure 결과 저장 ({timestamp})"],
            cwd=REPO_DIR, capture_output=True
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True)
        return _get_pages_url()
    except Exception as e:
        print(f"Allure 배포 실패: {e}")
        return None


def _check_unrefunded_payments():
    """결제 내역에서 미환불 거래 확인 (취소 완료 안 된 항목)"""
    driver = None
    try:
        driver = create_android_driver()
        time.sleep(3)
        close_any_popup(driver)

        try:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "더보기").click()
        except Exception:
            driver.back()
            time.sleep(1)
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "더보기").click()
        time.sleep(1)

        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "결제 내역").click()
        time.sleep(2)

        # "결제 완료" 상태 = 아직 환불 안 된 거래
        items = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("결제 완료")'
        )

        results = []
        for item in items:
            try:
                parent = item.find_element(AppiumBy.XPATH, "..")
                siblings = parent.find_elements(AppiumBy.XPATH, ".//*")
                texts = [s.text for s in siblings if s.text and s.text != "결제 완료"]
                results.append(" | ".join(texts[:3]) if texts else "거래 정보 없음")
            except Exception:
                results.append("미환불 거래 발견")

        return results
    except Exception as e:
        print(f"환불 확인 실패: {e}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def close_any_popup(driver):
    """팝업/모달이 있으면 확인 버튼으로 닫기"""
    for locator in [
        (AppiumBy.ACCESSIBILITY_ID, "확인"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("확인")'),
    ]:
        try:
            driver.find_element(*locator).click()
            time.sleep(0.5)
            return
        except Exception:
            pass


@pytest.fixture
def driver():
    """테스트 전: 드라이버 생성 / 테스트 후: 드라이버 종료"""
    driver = create_android_driver()
    close_any_popup(driver)
    time.sleep(3)

    yield driver

    driver.quit()


@pytest.fixture
def driver_at_appium_category(driver):
    """appium 카테고리 화면에서 시작하는 fixture"""
    close_any_popup(driver)
    try:
        ProductFlow(driver).go_to_appium_category()
    except Exception:
        # 결제 내역 등 하위 화면에 있는 경우 뒤로가기 후 재시도
        driver.back()
        time.sleep(0.5)
        close_any_popup(driver)
        ProductFlow(driver).go_to_appium_category()
    return driver


def pytest_addoption(parser):
    parser.addoption("--slack", action="store_true", default=False, help="테스트 결과를 Slack으로 전송")


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
    if session.config.getoption("--slack"):
        report_url = _deploy_allure_report()
        unrefunded = _check_unrefunded_payments()
        send_test_results(r["passed"], r["failed"], r["error"], duration, r["failures"], report_url, unrefunded)
    del pytest._qa_results
