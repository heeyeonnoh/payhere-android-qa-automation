from appium.webdriver.common.appiumby import AppiumBy
from ..utils.wait_utils import wait_for_clickable


class PaymentPage:
    def __init__(self, driver):
        self.driver = driver

    # 결제 수단
    CARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "카드")
    CASH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "현금")

    # 금액 버튼
    UNDER_50K = (AppiumBy.ACCESSIBILITY_ID, "5만원 미만")
    EXACT_50K = (AppiumBy.ACCESSIBILITY_ID, "5만원")
    OVER_50K = (AppiumBy.ACCESSIBILITY_ID, "5만원 이상")

    # 결제 버튼
    PAY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "결제")

    def select_card(self):
        wait_for_clickable(self.driver, *self.CARD_BUTTON).click()

    def select_cash(self):
        wait_for_clickable(self.driver, *self.CASH_BUTTON).click()

    def select_under_50k(self):
        wait_for_clickable(self.driver, *self.UNDER_50K).click()

    def select_50k(self):
        wait_for_clickable(self.driver, *self.EXACT_50K).click()

    def select_over_50k(self):
        wait_for_clickable(self.driver, *self.OVER_50K).click()

    def click_pay(self):
        wait_for_clickable(self.driver, *self.PAY_BUTTON).click()
