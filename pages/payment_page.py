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
    MARKET_PRICE_PRODUCT = (AppiumBy.ACCESSIBILITY_ID, "시가, 시가")
    UNIT_PRODUCT = (AppiumBy.ACCESSIBILITY_ID, "단위, 단위")

    # 시가/단위 입력 후 적용
    APPLY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "적용")

    # 오른쪽 숫자 키패드 좌표 (1920×1200 기준)
    INPUT_KEYPAD = {
        '1': (1273, 266), '2': (1440, 266), '3': (1606, 266),
        '4': (1273, 440), '5': (1440, 440), '6': (1606, 440),
        '7': (1273, 614), '8': (1440, 614), '9': (1606, 614),
        '0': (1440, 787), 'C': (1273, 787), '.': (1273, 787),
    }

    # 결제 버튼 (동적 - 텍스트에 "결제" 포함)
    PAY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("결제")')

    # 결제 방법 locator
    CARD_PAYMENT = (AppiumBy.ACCESSIBILITY_ID, "카드 결제")
    CASH_PAYMENT = (AppiumBy.ACCESSIBILITY_ID, "현금 결제")

    # 할부 선택 모달 (5만원 이상)
    INSTALLMENT_LUMP_SUM = (AppiumBy.ACCESSIBILITY_ID, "일시불")
    INSTALLMENT_MONTH_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().hintText("할부 개월수를 입력해 주세요.")'
    )
    INSTALLMENT_MONTH_FIELD_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.EditText[@hint="할부 개월수를 입력해 주세요."]'
    )
    INSTALLMENT_MONTH_FIELD_CLASSNAME = (
        AppiumBy.CLASS_NAME,
        "android.widget.EditText"
    )
    INSTALLMENT_2_MONTH = (AppiumBy.ACCESSIBILITY_ID, "2개월")
    INSTALLMENT_2_MONTH_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("2개월")'
    )
    INSTALLMENT_PAY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "결제")
    INSTALLMENT_SELECTED_2_MONTH = (AppiumBy.ACCESSIBILITY_ID, "2개월")
    INSTALLMENT_PAY_BUTTON_COORDS = (960, 1044)

    # 서명 (5만원 초과)
    SIGN_IN_SELLER_APP = (AppiumBy.ACCESSIBILITY_ID, "셀러앱에서 서명")
    SIGN_IN_SELLER_APP_DESC = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("셀러앱에서 서명")'
    )

    # 현금 결제 완료 버튼
    CASH_COMPLETE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "결제 완료")

    # 할인/포인트 버튼
    DISCOUNT_COUPON_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "할인/쿠폰")
    POINTS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "포인트/회원권")

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

    def select_market_price_product(self):
        wait_for_visible(self.driver, *self.MARKET_PRICE_PRODUCT).click()
        time.sleep(0.5)

    def select_unit_product(self):
        wait_for_visible(self.driver, *self.UNIT_PRODUCT).click()
        time.sleep(0.5)

    def enter_market_price(self, price: str):
        """시가 입력 모달에서 오른쪽 키패드로 가격 입력 (기본값 0 클리어 후 입력)"""
        self.driver.tap([(1273, 787)])  # C
        time.sleep(0.3)
        for digit in price:
            x, y = self.INPUT_KEYPAD[digit]
            self.driver.tap([(x, y)])
            time.sleep(0.2)

    def enter_unit_qty(self, qty: str):
        """단위 입력 모달에서 오른쪽 키패드로 총량 입력"""
        for ch in qty:
            x, y = self.INPUT_KEYPAD[ch]
            self.driver.tap([(x, y)])
            time.sleep(0.2)

    def click_apply_button(self):
        wait_for_visible(self.driver, *self.APPLY_BUTTON).click()
        time.sleep(0.5)

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

    def _click_first_available(self, locators, timeout=10):
        end_time = time.time() + timeout
        last_error = None

        while time.time() < end_time:
            for locator in locators:
                try:
                    self.driver.find_element(*locator).click()
                    return True
                except Exception as e:
                    last_error = e
            time.sleep(0.5)

        if last_error:
            raise last_error
        return False

    def _select_2_month_installment(self):
        """할부 드롭다운 클릭 후 2개월 좌표 탭.

        드롭다운 항목이 React Native lazy 렌더링으로 accessibility tree에 노출되지
        않으므로 좌표로 직접 탭한다. (일시불→직접입력→2개월 순서, 항목 높이 ≈98px)
        """
        wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM, timeout=30).click()
        time.sleep(1)
        self.driver.tap([(960, 875)])
        time.sleep(0.5)

    def select_installment_2m_and_pay(self):
        """할부 선택 모달에서 2개월 할부 선택 후 결제 (5만원 - 서명 불필요)"""
        self._select_2_month_installment()
        try:
            wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON, timeout=5).click()
        except Exception:
            self.driver.tap([self.INSTALLMENT_PAY_BUTTON_COORDS])

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

    def sign_and_pay(self):
        """일시불 선택 + 서명 후 결제 (5만원 초과)"""
        wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM).click()
        wait_for_visible(self.driver, *self.SIGN_IN_SELLER_APP).click()
        time.sleep(0.5)
        self._draw_signature()
        wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON).click()

    def sign_and_pay_installment(self):
        """2개월 할부 선택 + 서명 후 결제 (5만원 초과)"""
        self._select_2_month_installment()
        self._click_first_available(
            [self.SIGN_IN_SELLER_APP, self.SIGN_IN_SELLER_APP_DESC],
            timeout=15
        )
        time.sleep(0.5)
        self._draw_signature()
        try:
            wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON, timeout=5).click()
        except Exception:
            self.driver.tap([self.INSTALLMENT_PAY_BUTTON_COORDS])

    def click_cash_complete_button(self):
        """현금 결제 완료 버튼 클릭"""
        wait_for_visible(self.driver, *self.CASH_COMPLETE_BUTTON).click()

    def try_select_installment_and_pay(self, timeout: int = 4):
        """할부 선택 모달이 나타나면 일시불 선택 후 결제. 없으면 조용히 스킵."""
        try:
            wait_for_visible(self.driver, *self.INSTALLMENT_LUMP_SUM, timeout=timeout).click()
            try:
                wait_for_visible(self.driver, *self.INSTALLMENT_PAY_BUTTON, timeout=timeout).click()
            except Exception:
                self.driver.tap([self.INSTALLMENT_PAY_BUTTON_COORDS])
        except Exception:
            pass

    def click_discount_coupon_button(self):
        wait_for_visible(self.driver, *self.DISCOUNT_COUPON_BUTTON).click()

    def click_points_button(self):
        wait_for_visible(self.driver, *self.POINTS_BUTTON).click()

    def click_confirm_button(self):
        wait_for_visible(self.driver, *self.CONFIRM_BUTTON, timeout=30).click()
