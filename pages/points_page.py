from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible
import time

KEYPAD = {
    '1': (1273, 266), '2': (1440, 266), '3': (1606, 266),
    '4': (1273, 440), '5': (1440, 440), '6': (1606, 440),
    '7': (1273, 614), '8': (1440, 614), '9': (1606, 614),
    '0': (1440, 787), 'C': (1273, 787),
}


class PointsPage:
    APP_INPUT = (AppiumBy.ACCESSIBILITY_ID, "앱에서 입력")
    SEARCH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "조회")
    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "확인")
    APPLY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "적용")

    def __init__(self, driver):
        self.driver = driver

    def _enter_digits_in_field(self, field_index: int, digits: str):
        fields = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        fields[field_index].click()
        time.sleep(0.3)
        for d in digits:
            x, y = KEYPAD[d]
            self.driver.tap([(x, y)])
            time.sleep(0.2)

    def apply_points(self, phone_last4: str = "7745", amount: str = "1000"):
        wait_for_visible(self.driver, *self.APP_INPUT).click()
        time.sleep(1)

        # Enter last 4 digits of phone number
        self._enter_digits_in_field(0, phone_last4)
        wait_for_visible(self.driver, *self.SEARCH_BUTTON).click()
        time.sleep(1.5)

        # Confirm customer profile (고객 조회)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()
        time.sleep(1.5)

        # Enter points amount in 사용 포인트 field (index 1)
        self._enter_digits_in_field(1, amount)

        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(1)
