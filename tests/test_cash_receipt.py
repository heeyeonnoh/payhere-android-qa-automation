import pytest
import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

PHONE = "01012345678"


@allure.feature("현금영수증")
@allure.story("현금 결제 → 현금영수증 발급 → 환불 (영수증 취소)")
def test_cash_payment_with_receipt_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_under_50k_with_receipt(PHONE)
    RefundFlow(driver_at_appium_category).refund_with_cash_receipt(PHONE)
