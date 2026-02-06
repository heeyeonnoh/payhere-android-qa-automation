from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible


class PaymentPage:
    def __init__(self, driver):
        self.driver = driver

    PRODUCT_UNDER_50K = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("5만원 미만 x1")'
    )

    PAY_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("결제")'
    )

    CARD_PAYMENT_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "카드 결제"
    )

    def select_under_50k_product(self):
        wait_for_visible(self.driver, *self.PRODUCT_UNDER_50K).click()

    def click_pay_button(self):
        wait_for_visible(self.driver, *self.PAY_BUTTON).click()

    def select_card_payment(self):
        wait_for_visible(self.driver, *self.CARD_PAYMENT_BUTTON).click()
