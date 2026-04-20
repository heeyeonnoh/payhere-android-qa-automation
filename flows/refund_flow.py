from pages.refund_page import RefundPage


class RefundFlow:
    def __init__(self, driver):
        self.page = RefundPage(driver)

    def refund_latest_payment(self):
        """가장 최근 결제 환불"""
        self.page.go_to_more_tab()
        self.page.go_to_payment_history()
        self.page.select_latest_payment()
        self.page.click_refund_button()
        self.page.click_refund_confirm()
        self.page.click_refund_final()
