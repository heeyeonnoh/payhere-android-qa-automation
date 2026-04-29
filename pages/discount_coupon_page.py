from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible
import time

KEYPAD = {
    '1': (1273, 266), '2': (1440, 266), '3': (1606, 266),
    '4': (1273, 440), '5': (1440, 440), '6': (1606, 440),
    '7': (1273, 614), '8': (1440, 614), '9': (1606, 614),
    '0': (1440, 787), 'C': (1273, 787),
}


class DiscountCouponPage:
    COUPON_TAB = (AppiumBy.ACCESSIBILITY_ID, "쿠폰 할인")
    SELLER_INPUT = (AppiumBy.ACCESSIBILITY_ID, "셀러에서 입력")
    SEARCH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "조회")
    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "확인")
    APPLY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "적용")

    def __init__(self, driver):
        self.driver = driver

    def _enter_digits(self, digits: str):
        self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").click()
        time.sleep(0.3)
        for d in digits:
            x, y = KEYPAD[d]
            self.driver.tap([(x, y)])
            time.sleep(0.2)

    def apply_coupon(self, phone_last4: str = "7745"):
        wait_for_visible(self.driver, *self.COUPON_TAB).click()
        time.sleep(0.5)
        wait_for_visible(self.driver, *self.SELLER_INPUT).click()
        time.sleep(1)

        self._enter_digits(phone_last4)
        wait_for_visible(self.driver, *self.SEARCH_BUTTON).click()
        time.sleep(1.5)

        # Select customer from search results list
        results = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{phone_last4}")'
        )
        results[0].click()
        time.sleep(1.5)

        # Confirm customer profile (고객 조회)
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON).click()
        time.sleep(1.5)

        # Select first available coupon (쿠폰 조회)
        coupons = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("사용가능")'
        )
        coupons[0].click()
        time.sleep(0.5)

        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(1)
