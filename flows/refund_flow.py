import time
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
        """현금영수증 발급된 현금 결제 환불 (개인 영수증 번호 입력 후 발급 취소)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        CashReceiptPage(self.page.driver).cancel_receipt(phone)
        self.page.go_back_to_main()

    def refund_with_business_receipt(self, business_number="1234567890"):
        """사업자 현금영수증 발급된 현금 결제 환불 (사업자 번호 입력 후 발급 취소)"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        CashReceiptPage(self.page.driver).cancel_business_receipt(business_number)
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

    def refund_split_dutch_payments(self):
        """분할결제/더치페이: 최신 결제 환불 후 남은 분할 슬롯을 모두 환불"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
        self.page.click_refund_success_confirm()

        for _ in range(5):
            self.page.go_to_payment_history_fresh()
            if not self.page.select_first_unrefunded_payment():
                break
            self.page.wait_for_refund_detail_loaded()
            self.page.click_refund_button()
            self.page.click_refund_confirm()
            self.page.click_refund_final()
            self.page.click_refund_success_confirm()

        self.page.go_back_to_main()
