from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible
import time

KEYPAD = {
    '1': (1273, 266), '2': (1440, 266), '3': (1606, 266),
    '4': (1273, 440), '5': (1440, 440), '6': (1606, 440),
    '7': (1273, 614), '8': (1440, 614), '9': (1606, 614),
    '0': (1440, 787), 'C': (1273, 787),
}


class SplitPaymentPage:
    SPLIT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "분할 결제")
    DIRECT_INPUT_TAB = (AppiumBy.ACCESSIBILITY_ID, "직접 입력")
    DUTCH_PAY_TAB = (AppiumBy.ACCESSIBILITY_ID, "더치 페이")
    APPLY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "적용")
    CONTINUE_PAYMENT = (AppiumBy.ACCESSIBILITY_ID, "계속 결제")

    def __init__(self, driver):
        self.driver = driver

    def open_direct_split(self, amount: str):
        """직접 입력 탭에서 첫 번째 분할 금액 설정 후 적용"""
        wait_for_visible(self.driver, *self.SPLIT_BUTTON).click()
        time.sleep(0.5)
        wait_for_visible(self.driver, *self.DIRECT_INPUT_TAB).click()
        time.sleep(0.3)
        self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").click()
        time.sleep(0.3)
        for d in amount:
            x, y = KEYPAD[d]
            self.driver.tap([(x, y)])
            time.sleep(0.2)
        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(1)

    def open_dutch_pay(self):
        """더치 페이 탭 — 기본 2명 그대로 적용"""
        wait_for_visible(self.driver, *self.SPLIT_BUTTON).click()
        time.sleep(0.5)
        wait_for_visible(self.driver, *self.DUTCH_PAY_TAB).click()
        time.sleep(0.5)
        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(1)

    def continue_direct_split(self):
        """직접 입력 분할결제: 계속 결제 → 남은 금액 자동 입력된 분할 모달 → 적용"""
        wait_for_visible(self.driver, *self.CONTINUE_PAYMENT, timeout=30).click()
        time.sleep(1.5)
        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(1)

    def continue_dutch_pay(self):
        """더치페이: 계속 결제 → 결제 모달 바로 노출 (분할 모달 없음, 적용 불필요)"""
        wait_for_visible(self.driver, *self.CONTINUE_PAYMENT, timeout=30).click()
        time.sleep(1.5)
