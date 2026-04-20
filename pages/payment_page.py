from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible


class PaymentPage:
    UNDER_50K_PRODUCT = (
        AppiumBy.ACCESSIBILITY_ID,
        "5만원 미만, 0, 1,000원"
    )

    CARD_PAYMENT = (
        AppiumBy.ACCESSIBILITY_ID,
        "카드 결제"
    )

    def __init__(self, driver):
        self.driver = driver

    def select_under_50k_product(self):
        wait_for_visible(self.driver, *self.UNDER_50K_PRODUCT).click()

    def select_card_payment(self):
        wait_for_visible(self.driver, *self.CARD_PAYMENT).click()
