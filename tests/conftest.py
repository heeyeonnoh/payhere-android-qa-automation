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


def _get_unrefunded_list_items(driver):
    """결제 목록 왼쪽 패널에서 미환불 항목 반환.
    환불된 항목은 '환불' 뱃지 + '#번호', 미환불 항목은 '현금'/'카드' 텍스트만 표시됨."""
    result = []
    for method in ("현금", "카드"):
        els = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{method}")'
        )
        for el in els:
            if el.location["x"] < 100:
                result.append(el)
    result.sort(key=lambda el: el.location["y"])
    return result


def _get_detail_refund_info(driver):
    """상세 패널에서 현재 선택된 결제가 미환불인지 확인하고 (is_unrefunded, is_card, amount_text) 반환"""
    # "환불된 금액0원" 텍스트가 있으면 아직 한 번도 환불 안 된 상태
    is_unrefunded = bool(
        driver.find_elements(AppiumBy.XPATH, '//*[contains(@text, "환불된 금액0원")]')
    )
    if not is_unrefunded:
        return False, False, ""

    all_texts = [e.text for e in driver.find_elements(AppiumBy.XPATH, "//*[@text!='']") if e.text.strip()]
    full_text = " ".join(all_texts)

    is_card = "카드" in full_text
    # "합계X원" 혹은 "원" 포함 토큰 중 숫자가 있는 첫 번째 값
    amount_text = ""
    for t in all_texts:
        if "합계" in t and "원" in t:
            amount_text = t.replace("합계", "").strip()
            break
    if not amount_text:
        for t in all_texts:
            candidate = t.strip()
            if candidate.endswith("원") and any(c.isdigit() for c in candidate):
                amount_text = candidate
                break

    return True, is_card, amount_text


def _check_and_refund_unrefunded_payments():
    """최신 10건 결제 내역을 확인하고 미환불 거래 자동 환불 시도. (auto_refunded, still_unrefunded) 반환"""
    from pages.refund_page import RefundPage

    driver = None
    auto_refunded = []
    still_unrefunded = []

    try:
        driver = create_android_driver()
    except Exception as e:
        print(f"환불 확인 불가 (기기/Appium 연결 실패): {e}")
        return None, None

    try:
        time.sleep(3)
        # WebView 컨텍스트에 갇혀 있으면 NATIVE_APP으로 전환
        if driver.current_context != "NATIVE_APP":
            driver.switch_to.context("NATIVE_APP")
        # 네이티브 화면("더보기" 탭)이 보일 때까지 back()으로 탈출
        for _ in range(5):
            if driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "더보기"):
                break
            driver.back()
            time.sleep(2)
        page = RefundPage(driver)

        def _go_to_payment_history_fresh():
            for _ in range(5):
                if driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "더보기"):
                    break
                driver.back()
                time.sleep(2)
            page.go_to_more_tab()
            page.go_to_payment_history()
            time.sleep(3)

        for _ in range(10):  # 최대 10건
            _go_to_payment_history_fresh()

            unrefunded_els = _get_unrefunded_list_items(driver)
            if not unrefunded_els:
                break

            unrefunded_els[0].click()
            time.sleep(1.5)

            is_unrefunded, is_card, amount_text = _get_detail_refund_info(driver)
            if not is_unrefunded:
                continue

            try:
                over_50k = int(amount_text.replace(",", "").replace("원", "").strip()) > 50000
            except ValueError:
                over_50k = False

            try:
                page.click_refund_button()
                page.click_refund_confirm()
                page.click_refund_final()

                if is_card and over_50k:
                    page.sign_for_refund()

                page.click_refund_success_confirm()
                time.sleep(1)
                label = f"{'카드' if is_card else '현금'} {amount_text or '금액 미확인'}"
                auto_refunded.append(label)
                print(f"자동 환불 완료: {label}")

            except Exception as e:
                print(f"자동 환불 실패: {e}")

        # 재확인
        _go_to_payment_history_fresh()
        for el in _get_unrefunded_list_items(driver):
            el.click()
            time.sleep(1.5)
            is_unrefunded, is_card, amount_text = _get_detail_refund_info(driver)
            if is_unrefunded:
                label = f"{'카드' if is_card else '현금'} {amount_text or '금액 미확인'}"
                still_unrefunded.append(label)

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
    if not hasattr(pytest, "_qa_results"):
        pytest._qa_results = {
            "passed": 0, "failed": 0, "error": 0,
            "failures": [], "start": time.time(),
            "test_results": {}, "failure_reasons": {},
        }
    r = pytest._qa_results
    test_name = report.nodeid.split("::")[-1]

    if report.when == "call":
        if report.passed:
            r["passed"] += 1
            r["test_results"][test_name] = True
        elif report.failed:
            r["failed"] += 1
            reason = _extract_failure_reason(report.longrepr)
            r["failures"].append(f"{test_name}\n    → {reason}")
            r["test_results"][test_name] = False
            r["failure_reasons"][test_name] = reason
    elif report.when == "setup" and report.failed:
        r["error"] += 1
        reason = _extract_failure_reason(report.longrepr)
        r["failures"].append(f"{test_name}\n    → (setup) {reason}")
        r["test_results"][test_name] = False
        r["failure_reasons"][test_name] = f"(setup) {reason}"


def pytest_sessionfinish(session, exitstatus):
    if not hasattr(pytest, "_qa_results"):
        return
    r = pytest._qa_results
    duration = time.time() - r["start"]

    # 마지막 실행 결과를 JSON으로 저장 (TestRail 업데이트 요청 시 사용)
    import json as _json
    result_path = os.path.join(REPO_DIR, "last_test_results.json")
    try:
        with open(result_path, "w", encoding="utf-8") as f:
            _json.dump({
                "test_results": r["test_results"],
                "failure_reasons": r["failure_reasons"],
                "run_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"결과 저장 실패: {e}")

    if session.config.getoption("--slack"):
        report_url, deploy_error = _deploy_allure_report()
        auto_refunded, still_unrefunded = _check_and_refund_unrefunded_payments()
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
