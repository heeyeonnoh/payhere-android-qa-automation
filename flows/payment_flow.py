from pages.payment_page import PaymentPage
from pages.cash_receipt_page import CashReceiptPage


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

    # 기존 메서드 (호환성)
    def card_payment_under_50k(self):
        self.card_under_50k()
