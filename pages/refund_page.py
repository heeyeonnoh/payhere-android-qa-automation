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

    # 서명 (5만원 초과 환불) - "카드 환불" 화면 하단 좌측 버튼
    SIGN_IN_SELLER_APP_COORDS = (670, 1036)
    REFUND_AFTER_SIGN_COORDS = (1249, 1036)  # 서명 후 활성화되는 "환불" 버튼

    def __init__(self, driver):
        self.driver = driver

    def go_to_more_tab(self):
        wait_for_visible(self.driver, *self.MORE_TAB).click()

    def go_to_payment_history(self):
        wait_for_visible(self.driver, *self.PAYMENT_HISTORY).click()

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
        """환불 완료 후 확인 버튼 클릭"""
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("확인")'
            )
            el.click()
            time.sleep(0.5)
        except Exception:
            pass

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

    def sign_for_refund(self):
        """5만원 초과 환불 - 카드 환불 화면에서 셀러앱 서명"""
        time.sleep(3)  # 화면이 "서명 대기 중"으로 전환될 때까지 대기
        self.driver.tap([self.SIGN_IN_SELLER_APP_COORDS])
        time.sleep(1)
        self._draw_signature()
        time.sleep(0.5)
        self.driver.tap([self.REFUND_AFTER_SIGN_COORDS])  # 서명 후 환불 버튼
        time.sleep(1)

    def go_back_to_main(self):
        """환불 후 결제 내역에서 뒤로가기"""
        self.driver.back()
        time.sleep(0.5)
