from pages.payment_page import PaymentPage
from pages.cash_receipt_page import CashReceiptPage
from pages.discount_coupon_page import DiscountCouponPage
from pages.points_page import PointsPage
from pages.split_payment_page import SplitPaymentPage


class PaymentFlow:
    def __init__(self, driver):
        self.page = PaymentPage(driver)

    # 카드 결제
    def card_under_50k(self):
        self.page.select_under_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.click_confirm_button()

    def card_50k(self):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.select_installment_and_pay()  # 할부 선택 모달
        self.page.click_confirm_button()

    def card_over_50k(self):
        self.page.select_over_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.sign_and_pay()  # 할부 선택 + 서명
        self.page.click_confirm_button()

    # 현금 결제
    def cash_under_50k(self):
        self.page.select_under_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    def cash_50k(self):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    def cash_over_50k(self):
        self.page.select_over_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    # 카드 할부 결제
    def card_50k_installment(self):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.select_installment_2m_and_pay()
        self.page.click_confirm_button()

    def card_over_50k_installment(self):
        self.page.select_over_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.sign_and_pay_installment()
        self.page.click_confirm_button()

    # 현금 결제 + 현금영수증 발급
    def cash_under_50k_with_receipt(self, phone="01012345678"):
        self.page.select_under_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        CashReceiptPage(self.page.driver).issue_receipt(phone)

    def cash_under_50k_with_business_receipt(self, business_number="1234567890"):
        self.page.select_under_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        CashReceiptPage(self.page.driver).issue_business_receipt(business_number)

    # 시가 상품 결제
    def card_market_price(self, price="2000"):
        self.page.select_market_price_product()
        self.page.enter_market_price(price)
        self.page.click_apply_button()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.click_confirm_button()

    def cash_market_price(self, price="2000"):
        self.page.select_market_price_product()
        self.page.enter_market_price(price)
        self.page.click_apply_button()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    # 단위 상품 결제
    def card_unit(self, qty="5"):
        self.page.select_unit_product()
        self.page.enter_unit_qty(qty)
        self.page.click_apply_button()
        self.page.click_pay_button()
        self.page.select_card_payment()
        self.page.click_confirm_button()

    def cash_unit(self, qty="5"):
        self.page.select_unit_product()
        self.page.enter_unit_qty(qty)
        self.page.click_apply_button()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    # 쿠폰 결제 (5만원 상품 기준 — 1,000원 쿠폰 적용 후 49,000원)
    def card_50k_with_coupon(self, phone_last4: str = "7745"):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.click_discount_coupon_button()
        DiscountCouponPage(self.page.driver).apply_coupon(phone_last4)
        self.page.select_card_payment()
        self.page.try_select_installment_and_pay()
        self.page.click_confirm_button()

    def cash_50k_with_coupon(self, phone_last4: str = "7745"):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.click_discount_coupon_button()
        DiscountCouponPage(self.page.driver).apply_coupon(phone_last4)
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    # 포인트 결제 (5만원 상품 기준 — 1,000P 차감 후 49,000원)
    def card_50k_with_points(self, phone_last4: str = "7745", points: str = "1000"):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.click_points_button()
        PointsPage(self.page.driver).apply_points(phone_last4, points)
        self.page.select_card_payment()
        self.page.try_select_installment_and_pay()
        self.page.click_confirm_button()

    def cash_50k_with_points(self, phone_last4: str = "7745", points: str = "1000"):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.click_points_button()
        PointsPage(self.page.driver).apply_points(phone_last4, points)
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        self.page.click_confirm_button()

    # 분할결제 — 직접 입력 (현금 → 카드)
    def split_cash_card(self, split_amount: str = "500"):
        """분할결제(직접 입력): 첫 번째 현금, 두 번째 카드"""
        self.page.select_50k_product()
        self.page.click_pay_button()
        sp = SplitPaymentPage(self.page.driver)
        sp.open_direct_split(split_amount)
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        sp.continue_direct_split()
        self.page.select_card_payment()
        self.page.click_confirm_button()

    def split_card_card(self, split_amount: str = "500"):
        """분할결제(직접 입력): 첫 번째 카드, 두 번째 카드"""
        self.page.select_50k_product()
        self.page.click_pay_button()
        sp = SplitPaymentPage(self.page.driver)
        sp.open_direct_split(split_amount)
        self.page.select_card_payment()
        self.page.try_select_installment_and_pay()
        sp.continue_direct_split()
        self.page.select_card_payment()
        self.page.click_confirm_button()

    # 더치페이 — 2명 균등 (현금 → 카드)
    def dutch_pay_cash_card(self):
        """더치페이 2명: 첫 번째 현금, 두 번째 카드"""
        self.page.select_50k_product()
        self.page.click_pay_button()
        sp = SplitPaymentPage(self.page.driver)
        sp.open_dutch_pay()
        self.page.select_cash_payment()
        self.page.click_cash_complete_button()
        sp.continue_dutch_pay()
        self.page.select_card_payment()
        self.page.try_select_installment_and_pay()
        self.page.click_confirm_button()

    # 기존 메서드 (호환성)
    def card_payment_under_50k(self):
        self.card_under_50k()
