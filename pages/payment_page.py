from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from utils.wait_utils import wait_for_visible
import time


class PaymentPage:
    # 상품 locator
    UNDER_50K_PRODUCT = (AppiumBy.ACCESSIBILITY_ID, "5만원 미만, 1,000원")
    PRODUCT_50K = (AppiumBy.ACCESSIBILITY_ID, "5만원, 50,000원")
    OVER_50K_PRODUCT = (AppiumBy.ACCESSIBILITY_ID, "5만원 이상, 50,001원")

    # 결제 버튼 (동적 - 텍스트에 "결제" 포함)
    PAY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("결제")')

    # 결제 방법 locator
    CARD_PAYMENT = (AppiumBy.ACCESSIBILITY_ID, "카드 결제")
    CASH_PAYMENT = (AppiumBy.ACCESSIBILITY_ID, "현금 결제")

    # 할부 선택 모달 (5만원 이상)
    INSTALLMENT_LUMP_SUM = (AppiumBy.ACCESSIBILITY_ID, "일시불")
    INSTALLMENT_PAY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "결제")

    # 서명 (5만원 초과)
    SIGN_IN_SELLER_APP = (AppiumBy.ACCESSIBILITY_ID, "셀러앱에서 서명")

    # 현금 결제 완료 버튼
    CASH_COMPLETE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "결제 완료")

    # 결제 완료 확인 버튼
    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "확인")

    def __init__(self, driver):
        self.driver = driver

    # 상품 선택
    def select_under_50k_product(self):
        wait_for_visible(self.driver, *self.UNDER_50K_PRODUCT).click()

    def select_50k_product(self):
        wait_for_visible(self.driver, *self.PRODUCT_50K).click()

    def select_over_50k_product(self):
        wait_for_visible(self.driver, *self.OVER_50K_PRODUCT).click()

    # 결제 버튼
    def click_pay_button(self):
        wait_for_visible(self.driver, *self.PAY_BUTTON).click()

    # 결제 방법 선택
    def select_card_payment(self):
        wait_for_visible(self.driver, *self.CARD_PAYMENT).click()

    def select_cash_payment(self):
        wait_for_visible(self.driver, *self.CASH_PAYMENT).click()

    def select_installment_and_pay(self):
        """할부 선택 모달에서 일시불 선택 후 결제 (5만원)"""
        wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM).click()
        wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON).click()

    def sign_and_pay(self):
        """서명 후 결제 (5만원 초과)"""
        # 일시불 선택
        wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM).click()

        # 셀러앱에서 서명 클릭
        wait_for_visible(self.driver, *self.SIGN_IN_SELLER_APP).click()
        time.sleep(0.5)

        # 서명 (터치 액션)
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

        # 결제 버튼 클릭
        wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON).click()

    def click_cash_complete_button(self):
        """현금 결제 완료 버튼 클릭"""
        wait_for_visible(self.driver, *self.CASH_COMPLETE_BUTTON).click()

    def click_confirm_button(self):
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON, timeout=30).click()
