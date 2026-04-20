from pages.payment_page import PaymentPage


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
        self.page.click_confirm_button()

    def cash_50k(self):
        self.page.select_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        self.page.click_confirm_button()

    def cash_over_50k(self):
        self.page.select_over_50k_product()
        self.page.click_pay_button()
        self.page.select_cash_payment()
        # 현금은 서명 없음
        self.page.click_confirm_button()

    # 기존 메서드 (호환성)
    def card_payment_under_50k(self):
        self.card_under_50k()
