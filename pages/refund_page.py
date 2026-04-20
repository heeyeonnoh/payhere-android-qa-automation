from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        time.sleep(0.5)

    def click_refund_confirm(self):
        """하단 환불 확인 버튼 클릭"""
        self.driver.tap([self.REFUND_CONFIRM_COORDS])
        time.sleep(0.5)

    def click_refund_final(self):
        """대화상자 환불 버튼 클릭"""
        self.driver.tap([self.REFUND_FINAL_COORDS])
        time.sleep(1)
