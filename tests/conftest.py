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
from selenium.common.exceptions import WebDriverException
from driver.appium_driver import create_android_driver
from flows.product_flow import ProductFlow
from utils.slack_notifier import send_test_results

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PACKAGE = "in.payhere.prd"


def _get_pages_url():
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, cwd=REPO_DIR
        )
        url = result.stdout.strip()
        # SSH:   git@github.com:owner/repo.git → owner/repo
        # HTTPS: https://github.com/owner/repo.git → owner/repo
        if url.startswith("git@github.com:"):
            path = url.replace("git@github.com:", "").replace(".git", "")
        else:
            path = url.replace("https://github.com/", "").replace(".git", "")
        owner, repo = path.split("/")
        return f"https://{owner}.github.io/{repo}/"
    except Exception:
        return None


def _deploy_allure_report():
    step = "init"
    try:
        step = "allure generate"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        history_store = os.path.join(REPO_DIR, "allure-history")
        allure_tmp = os.path.join(REPO_DIR, "allure-tmp")
        # 저장된 히스토리를 allure-tmp/history에 복사 → 트렌드 반영
        if os.path.exists(history_store):
            history_for_report = os.path.join(allure_tmp, "history")
            if os.path.exists(history_for_report):
                shutil.rmtree(history_for_report)
            shutil.copytree(history_store, history_for_report)
        r = subprocess.run(
            ["allure", "generate", "allure-tmp", "--clean", "-o", "allure-report"],
            capture_output=True, cwd=REPO_DIR
        )
        if r.returncode != 0:
            raise RuntimeError(f"allure generate 실패: {r.stderr.decode(errors='ignore')[:200]}")
        # 새 히스토리를 allure-history에 저장 → 다음 실행에 사용
        new_history = os.path.join(REPO_DIR, "allure-report", "history")
        if os.path.exists(new_history):
            if os.path.exists(history_store):
                shutil.rmtree(history_store)
            shutil.copytree(new_history, history_store)
        # 날짜+시간 폴더에 결과 저장
        step = "archive"
        archive_dir = os.path.join(REPO_DIR, "allure-results", timestamp)
        if os.path.exists(archive_dir):
            shutil.rmtree(archive_dir)
        shutil.copytree(allure_tmp, archive_dir)
        step = "ghp_import"
        result = subprocess.run(
            [sys.executable, "-m", "ghp_import", "-n", "-p", "-f", "allure-report"],
            capture_output=True, text=True, cwd=REPO_DIR
        )
        if result.returncode != 0:
            raise RuntimeError(f"ghp_import 실패: {result.stderr[:200]}")
        # allure-results/{timestamp} + allure-history를 main 브랜치에 커밋 & 푸시
        step = "git push"
        subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                       cwd=REPO_DIR, capture_output=True)
        subprocess.run(["git", "add", f"allure-results/{timestamp}/", "allure-history/"], cwd=REPO_DIR)
        subprocess.run(
            ["git", "commit", "-m", f"test: Allure 결과 저장 ({timestamp})"],
            cwd=REPO_DIR, capture_output=True
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True)
        return _get_pages_url(), None
    except Exception as e:
        err = f"[{step}] {e}"
        print(f"Allure 배포 실패: {err}")
        return None, err


def _go_to_payment_history(driver):
    """더보기 → 결제 내역 이동"""
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


def _get_unrefunded_items(driver):
    """결제 내역에서 '결제 완료' 상태(미환불) 항목 반환"""
    return driver.find_elements(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("결제 완료")'
    )


def _check_and_refund_unrefunded_payments():
    """미환불 거래 확인 후 자동 환불 시도. (auto_refunded, still_unrefunded) 반환"""
    from pages.refund_page import RefundPage

    driver = None
    auto_refunded = []
    still_unrefunded = []

    try:
        driver = create_android_driver()
    except Exception as e:
        print(f"환불 확인 불가 (기기/Appium 연결 실패): {e}")
        return None, None  # 기기 없음 → 확인 자체 불가

    try:
        time.sleep(3)
        _go_to_payment_history(driver)

        for _ in range(10):  # 최대 10건
            items = _get_unrefunded_items(driver)
            if not items:
                break

            try:
                # 클릭 가능한 상위 요소(행) 찾아서 진입
                row = items[0].find_element(
                    AppiumBy.XPATH, "ancestor::*[@clickable='true'][1]"
                )
                row.click()
                time.sleep(1.5)

                # 상세 화면에서 금액 읽기 (50,001원 초과 여부)
                amount_text = ""
                try:
                    els = driver.find_elements(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().textContains("원")'
                    )
                    if els:
                        amount_text = els[0].text
                except Exception:
                    pass

                page = RefundPage(driver)
                page.click_refund_button()
                page.click_refund_confirm()
                page.click_refund_final()

                # 50,001원 이상은 서명 필요
                over_50k = any(x in amount_text.replace(",", "") for x in ["50001", "50002", "50003"])
                if over_50k:
                    page.sign_for_refund()

                page.click_refund_success_confirm()
                driver.back()
                time.sleep(1)
                auto_refunded.append(amount_text or "금액 미확인")

            except Exception as e:
                print(f"자동 환불 실패: {e}")
                driver.back()
                time.sleep(1)
                break

        # 환불 후 남은 미환불 거래 확인
        for item in _get_unrefunded_items(driver):
            try:
                parent = item.find_element(AppiumBy.XPATH, "..")
                texts = [s.text for s in parent.find_elements(AppiumBy.XPATH, ".//*")
                         if s.text and s.text != "결제 완료"]
                still_unrefunded.append(" | ".join(texts[:3]) or "거래 정보 없음")
            except Exception:
                still_unrefunded.append("미환불 거래")

        return auto_refunded, still_unrefunded

    except Exception as e:
        print(f"환불 확인/시도 실패: {e}")
        return auto_refunded, still_unrefunded
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def close_any_popup(driver):
    """팝업/모달이 있으면 닫기 (확인 또는 취소)"""
    for locator in [
        (AppiumBy.ACCESSIBILITY_ID, "확인"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("확인")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("취소")'),
    ]:
        try:
            driver.find_element(*locator).click()
            time.sleep(0.5)
            return
        except Exception:
            pass


def close_blocking_modal(driver):
    """결제/환불 모달이 남아 있으면 우상단 닫기 버튼으로 정리"""
    modal_titles = ["카드 결제", "현금 결제", "카드 환불"]
    for title in modal_titles:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{title}")'
            )
            driver.tap([(1525, 50)])
            time.sleep(1)
            close_any_popup(driver)
            return True
        except Exception:
            pass
    return False


def recover_to_home(driver):
    """앱을 전면으로 가져오고 홈 탭 복귀를 시도한다."""
    try:
        driver.activate_app(APP_PACKAGE)
        time.sleep(2)
    except Exception:
        pass

    close_any_popup(driver)
    for _ in range(6):
        close_blocking_modal(driver)
        try:
            driver.hide_keyboard()
        except Exception:
            pass
        try:
            driver.back()
        except Exception:
            break
        time.sleep(0.7)

    # 상품 탭 직접 클릭 시도
    for _ in range(2):
        try:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, "상품").click()
            time.sleep(1)
            return
        except Exception:
            time.sleep(1)


@pytest.fixture
def driver():
    """테스트 전: 드라이버 생성 / 테스트 후: 드라이버 종료"""
    driver = create_android_driver()
    close_any_popup(driver)
    time.sleep(3)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


@pytest.fixture
def driver_at_appium_category(driver, request):
    """appium 카테고리 화면에서 시작하는 fixture"""
    close_any_popup(driver)
    # 이전 테스트가 WebView 서브화면에 남긴 경우 최대 4회 back() 시도
    for _ in range(6):
        try:
            close_blocking_modal(driver)
            ProductFlow(driver).go_to_appium_category()
            return driver
        except WebDriverException:
            try:
                driver.quit()
            except Exception:
                pass
            driver = create_android_driver()
            def _safe_quit(d=driver):
                try:
                    d.quit()
                except Exception:
                    pass
            request.addfinalizer(_safe_quit)
            close_any_popup(driver)
            recover_to_home(driver)
        except Exception:
            close_any_popup(driver)
            close_blocking_modal(driver)
            recover_to_home(driver)
            try:
                driver.back()
            except Exception:
                pass
            time.sleep(1)
    ProductFlow(driver).go_to_appium_category()
    return driver


def pytest_addoption(parser):
    parser.addoption("--slack", action="store_true", default=False, help="테스트 결과를 Slack으로 전송")


def _extract_failure_reason(longrepr):
    """traceback에서 실패 단계 + 에러 타입 추출"""
    text = str(longrepr)
    # 알려진 인프라 오류 먼저 확인
    if "연결된 Android 기기가 없습니다" in text:
        return "Android 기기 미연결"
    if "Connection refused" in text and "4723" in text:
        return "Appium 서버 미실행"
    if "WebDriverException" in text and "4723" in text:
        return "Appium 서버 연결 실패"
    try:
        lines = text.strip().split('\n')
        error_type = ""
        for line in reversed(lines):
            s = line.strip()
            if s.startswith('E '):
                msg = s.replace('E ', '', 1).strip()
                error_type = msg.split(':')[0].split('.')[-1]
                break
        step = ""
        for line in reversed(lines):
            if ' in ' in line and '.py:' in line:
                step = line.strip().split(' in ')[-1].strip()
                break
        if step and error_type:
            return f"{step} → {error_type}"
        return error_type or step or "알 수 없는 오류"
    except Exception:
        return "오류 정보 없음"


def pytest_runtest_logreport(report):
    if report.when == "call":
        if not hasattr(pytest, "_qa_results"):
            pytest._qa_results = {"passed": 0, "failed": 0, "error": 0, "failures": [], "start": time.time()}
        if report.passed:
            pytest._qa_results["passed"] += 1
        elif report.failed:
            pytest._qa_results["failed"] += 1
            reason = _extract_failure_reason(report.longrepr)
            test_name = report.nodeid.split("::")[-1]
            pytest._qa_results["failures"].append(f"{test_name}\n    → {reason}")
    elif report.when == "setup" and report.failed:
        if not hasattr(pytest, "_qa_results"):
            pytest._qa_results = {"passed": 0, "failed": 0, "error": 0, "failures": [], "start": time.time()}
        pytest._qa_results["error"] += 1
        reason = _extract_failure_reason(report.longrepr)
        test_name = report.nodeid.split("::")[-1]
        pytest._qa_results["failures"].append(f"{test_name}\n    → (setup) {reason}")


def pytest_sessionfinish(session, exitstatus):
    if not hasattr(pytest, "_qa_results"):
        return
    r = pytest._qa_results
    duration = time.time() - r["start"]
    if session.config.getoption("--slack"):
        report_url, deploy_error = _deploy_allure_report()
        auto_refunded, still_unrefunded = _check_and_refund_unrefunded_payments()
        # 동일한 실패 사유가 반복되면 대표 1건 + 나머지 건수로 압축
        failures = _compress_failures(r["failures"])
        send_test_results(r["passed"], r["failed"], r["error"], duration, failures, report_url, auto_refunded, still_unrefunded, deploy_error)
    del pytest._qa_results


def _compress_failures(failures: list[str]) -> list[str]:
    """동일 사유 반복 시 압축 (예: 기기 미연결 x6 → 1건으로)"""
    from collections import Counter
    # 사유 부분만 추출해서 카운트
    reasons = []
    for f in failures:
        parts = f.split("\n    → ")
        reasons.append(parts[-1] if len(parts) > 1 else f)
    reason_counts = Counter(reasons)
    if len(reason_counts) == 1 and len(failures) > 1:
        reason = list(reason_counts.keys())[0]
        return [f"전체 {len(failures)}건 동일 원인: {reason}"]
    return failures
