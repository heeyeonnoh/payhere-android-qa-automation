from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible
import time


class CashReceiptPage:
    CASH_RECEIPT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "현금 영수증 발급")
    SELLER_INPUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "셀러에서 입력")
    ISSUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "발급")
    CANCEL_ISSUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "발급 취소")
    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "확인")
    BUSINESS_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("사업자 (지출증빙)")')

    # 오른쪽 숫자 키패드 device 좌표 (1920×1200 기준)
    KEYPAD = {
        '1': (1273, 266), '2': (1440, 266), '3': (1606, 266),
        '4': (1273, 440), '5': (1440, 440), '6': (1606, 440),
        '7': (1273, 614), '8': (1440, 614), '9': (1606, 614),
        '0': (1440, 787),
    }

    def __init__(self, driver):
        self.driver = driver

    def _enter_number(self, number):
        wait_for_visible(self.driver, *self.SELLER_INPUT_BUTTON).click()
        time.sleep(0.5)
        for digit in number:
            x, y = self.KEYPAD[digit]
            self.driver.tap([(x, y)])
            time.sleep(0.3)

    def issue_receipt(self, phone="01012345678"):
        """결제 완료 화면에서 개인 현금영수증 발급 후 확인"""
        wait_for_visible(self.driver, *self.CASH_RECEIPT_BUTTON).click()
        self._enter_number(phone)
        wait_for_visible(self.driver, *self.ISSUE_BUTTON).click()
        time.sleep(1)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()

    def issue_business_receipt(self, business_number="1234567890"):
        """결제 완료 화면에서 사업자 현금영수증 발급 후 확인"""
        wait_for_visible(self.driver, *self.CASH_RECEIPT_BUTTON).click()
        wait_for_visible(self.driver, *self.BUSINESS_TAB).click()
        time.sleep(0.5)
        self._enter_number(business_number)
        wait_for_visible(self.driver, *self.ISSUE_BUTTON).click()
        time.sleep(1)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()

    def cancel_receipt(self, phone="01012345678"):
        """현금 환불 취소 화면에서 개인 영수증 번호 입력 후 발급 취소"""
        self._enter_number(phone)
        wait_for_visible(self.driver, *self.CANCEL_ISSUE_BUTTON).click()
        time.sleep(1)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()

    def cancel_business_receipt(self, business_number="1234567890"):
        """현금 환불 취소 화면에서 사업자 번호 입력 후 발급 취소"""
        wait_for_visible(self.driver, *self.BUSINESS_TAB).click()
        time.sleep(0.5)
        self._enter_number(business_number)
        wait_for_visible(self.driver, *self.CANCEL_ISSUE_BUTTON).click()
        time.sleep(1)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()
