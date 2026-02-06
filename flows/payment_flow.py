from ..pages.payment_page import PaymentPage


class PaymentFlow:
    def __init__(self, driver):
        self.page = PaymentPage(driver)

    # 카드 결제
    def card_under_50k(self):
        self.page.select_under_50k()
        self.page.select_card()
        self.page.click_pay()

    def card_50k(self):
        self.page.select_50k()
        self.page.select_card()
        self.page.click_pay()

    def card_over_50k(self):
        self.page.select_over_50k()
        self.page.select_card()
        self.page.click_pay()

    # 현금 결제
    def cash_under_50k(self):
        self.page.select_under_50k()
        self.page.select_cash()
        self.page.click_pay()

    def cash_50k(self):
        self.page.select_50k()
        self.page.select_cash()
        self.page.click_pay()

    def cash_over_50k(self):
        self.page.select_over_50k()
        self.page.select_cash()
        self.page.click_pay()
