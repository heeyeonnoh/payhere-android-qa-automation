from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from utils.wait_utils import wait_for_visible
import time


class RefundPage:
    # 탭
    MORE_TAB = (AppiumBy.ACCESSIBILITY_ID, "더보기")

    # 더보기 메뉴
    PAYMENT_HISTORY = (AppiumBy.ACCESSIBILITY_ID, "결제 내역")

    # 환불 버튼 (좌표 기반 - WebView 내부)
    REFUND_BUTTON_COORDS = (966, 627)  # 상세 화면의 환불 버튼
    REFUND_CONFIRM_COORDS = (960, 1044)  # 하단 환불 확인 버튼
    REFUND_FINAL_COORDS = (1162, 735)  # 대화상자 환불 버튼

    # 할부 선택 (5만원 환불)
    INSTALLMENT_LUMP_SUM = (AppiumBy.ACCESSIBILITY_ID, "일시불")
    INSTALLMENT_CONFIRM = (AppiumBy.ACCESSIBILITY_ID, "결제")

    # 서명 (5만원 초과 환불)
    CARD_REFUND_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("카드 환불")'
    )
    SIGN_IN_SELLER_APP = (AppiumBy.ACCESSIBILITY_ID, "셀러앱에서 서명")
    WAITING_FOR_SIGNATURE_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("서명 대기 중")'
    )
    SIGNATURE_GUIDE_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("서명해 주세요.")'
    )
    REFUND_AFTER_SIGN = (AppiumBy.ACCESSIBILITY_ID, "환불")
    REFUND_AFTER_SIGN_COORDS = (1249, 1036)  # 서명 후 활성화되는 "환불" 버튼
    REFUND_SUCCESS_CONFIRM_COORDS = (960, 1044)  # 취소 완료 모달의 "확인" 버튼

    def __init__(self, driver):
        self.driver = driver

    def go_to_payment_history_fresh(self):
        """현재 화면에서 back()으로 WebView 탈출 후 결제 내역 진입"""
        for _ in range(5):
            if self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "더보기"):
                break
            self.driver.back()
            time.sleep(2)
        self.go_to_more_tab()
        self.go_to_payment_history()
        time.sleep(3)

    def go_to_more_tab(self):
        time.sleep(2)
        # 결제 완료 모달의 "확인" 버튼이 남아있으면 클릭
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "확인").click()
            time.sleep(1)
        except Exception:
            pass
        wait_for_visible(self.driver, *self.MORE_TAB, timeout=15).click()

    def go_to_payment_history(self):
        wait_for_visible(self.driver, *self.PAYMENT_HISTORY).click()

    def wait_for_refund_detail_loaded(self, timeout: int = 10):
        """상세 패널에 '환불된 금액' 텍스트가 나타날 때까지 대기 (미환불 상세 로드 확인)"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, '//*[contains(@text, "환불된 금액")]')
                )
            )
        except Exception:
            time.sleep(3)

    def select_first_unrefunded_payment(self):
        """결제 목록에서 미환불 항목(현금/카드 뱃지, x<100) 첫 번째 선택. 있으면 True 반환."""
        time.sleep(1)
        for method in ("현금", "카드"):
            els = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{method}")'
            )
            for el in els:
                if el.location["x"] < 100:
                    el.click()
                    return True
        return False

    def select_latest_payment(self):
        """가장 최근 결제 내역 선택 (첫 번째 항목)"""
        time.sleep(1)
        # 결제 내역에서 첫 번째 결제 완료 항목 클릭
        try:
            # #으로 시작하는 첫 번째 결제 번호 찾기
            items = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textStartsWith("#")'
            )
            if items:
                items[0].click()
        except:
            pass
        time.sleep(0.5)

    def click_refund_button(self):
        """상세 화면의 환불 버튼 클릭"""
        self.driver.tap([self.REFUND_BUTTON_COORDS])
        time.sleep(1.5)

    def click_refund_confirm(self):
        """하단 환불 확인 버튼 클릭"""
        self.driver.tap([self.REFUND_CONFIRM_COORDS])
        time.sleep(0.5)

    def click_refund_final(self):
        """대화상자 환불 버튼 클릭"""
        self.driver.tap([self.REFUND_FINAL_COORDS])
        time.sleep(1)

    def click_refund_success_confirm(self):
        """환불(취소) 완료 모달의 확인 버튼 클릭"""
        time.sleep(15)  # 카드 취소 처리 완료까지 대기 (~10초 소요)
        self.driver.tap([self.REFUND_SUCCESS_CONFIRM_COORDS])
        time.sleep(0.5)

    def select_installment_for_refund(self):
        """5만원 환불 시 일시불 선택"""
        time.sleep(1)
        wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM).click()
        wait_for_visible(self.driver, *self.INSTALLMENT_CONFIRM).click()
        time.sleep(0.5)

    def _draw_signature(self):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver,
            mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(500, 800)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(1400, 800)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()
        time.sleep(0.5)

    def _draw_refund_signature(self):
        """카드 환불 모달의 서명 패드 영역에 직접 서명한다."""
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver,
            mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(560, 620)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(820, 720)
        actions.w3c_actions.pointer_action.move_to_location(1100, 560)
        actions.w3c_actions.pointer_action.move_to_location(1380, 700)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()
        time.sleep(0.5)

    def _click_first_available(self, locators, timeout=20):
        """여러 locator 중 먼저 보이는 요소 클릭. WebView/모달 차이를 흡수한다."""
        end_time = time.time() + timeout
        last_error = None

        while time.time() < end_time:
            for locator in locators:
                try:
                    self.driver.find_element(*locator).click()
                    return True
                except Exception as e:
                    last_error = e
            time.sleep(0.5)

        if last_error:
            raise last_error
        return False

    def _is_any_visible(self, locators):
        for locator in locators:
            try:
                elements = self.driver.find_elements(*locator)
                if any(element.is_displayed() for element in elements):
                    return locator
            except Exception:
                pass
        return None

    def sign_for_refund(self):
        """5만원 초과 환불 - 카드 환불 화면에서 셀러앱 서명"""
        # 최종 환불 이후 카드 환불 모달이 늦게 뜰 수 있어 제목부터 안정적으로 기다린다.
        wait_for_visible(self.driver, *self.CARD_REFUND_TITLE, timeout=25)

        state_locators = [
            self.SIGNATURE_GUIDE_TEXT,
            self.WAITING_FOR_SIGNATURE_TEXT,
            self.SIGN_IN_SELLER_APP,
        ]
        visible_state = None
        end_time = time.time() + 25
        while time.time() < end_time and visible_state is None:
            visible_state = self._is_any_visible(state_locators)
            if visible_state is None:
                time.sleep(0.5)

        if visible_state == self.SIGN_IN_SELLER_APP or visible_state == self.WAITING_FOR_SIGNATURE_TEXT:
            wait_for_visible(self.driver, *self.SIGN_IN_SELLER_APP, timeout=10).click()
            wait_for_visible(self.driver, *self.SIGNATURE_GUIDE_TEXT, timeout=10)
        elif visible_state != self.SIGNATURE_GUIDE_TEXT:
            raise TimeoutError("카드 환불 서명 상태를 확인하지 못했습니다.")

        self._draw_refund_signature()
        time.sleep(0.5)

        try:
            self._click_first_available([self.REFUND_AFTER_SIGN], timeout=5)
        except Exception:
            self.driver.tap([self.REFUND_AFTER_SIGN_COORDS])
        time.sleep(1)

    def go_back_to_main(self):
        """환불 후 결제 내역 → 더보기 메뉴까지 뒤로가기 (WebView 탈출)"""
        self.driver.back()  # 결제 상세 → 결제 내역 리스트
        time.sleep(0.5)
        self.driver.back()  # 결제 내역 리스트 → 더보기 메뉴 (네이티브)
        time.sleep(0.5)
