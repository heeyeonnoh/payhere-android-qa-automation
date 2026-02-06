from pages.payment_page import PaymentPage


class PaymentFlow:
    def __init__(self, driver):
        self.page = PaymentPage(driver)

    def card_payment_under_50k(self):

        self.page.select_under_50k_product()
        self.page.click_pay_button()
        self.page.select_card_payment()
