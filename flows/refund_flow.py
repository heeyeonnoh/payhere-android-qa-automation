from pages.refund_page import RefundPage
from pages.cash_receipt_page import CashReceiptPage


class RefundFlow:
    def __init__(self, driver):
        self.page = RefundPage(driver)

    def refund_latest_payment(self):
        """가장 최근 결제 환불 (5만원 이하)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        self.page.click_refund_success_confirm()
        self.page.go_back_to_main()

    def refund_latest_payment_50k(self):
        """가장 최근 결제 환불 (5만원 일시불 - 서명 불필요)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        self.page.click_refund_success_confirm()
        self.page.go_back_to_main()

    def refund_with_cash_receipt(self, phone="01012345678"):
        """현금영수증 발급된 현금 결제 환불 (현금 결제 취소 화면에서 번호 입력)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        CashReceiptPage(self.page.driver).cancel_receipt(phone)
        self.page.go_back_to_main()

    def refund_latest_payment_over_50k(self):
        """가장 최근 결제 환불 (5만원 초과)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        self.page.sign_for_refund()
        self.page.click_refund_success_confirm()
        self.page.go_back_to_main()
