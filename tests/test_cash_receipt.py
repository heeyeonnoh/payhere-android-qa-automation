import pytest
import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

PHONE = "01012345678"
BUSINESS_NUMBER = "8618101475"


@allure.feature("현금영수증")
@allure.story("현금 결제 → 개인 현금영수증 발급 → 환불 (영수증 취소)")
def test_cash_payment_with_receipt_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_under_50k_with_receipt(PHONE)
    RefundFlow(driver_at_appium_category).refund_with_cash_receipt(PHONE)


@allure.feature("현금영수증")
@allure.story("현금 결제 → 사업자 현금영수증 발급 → 환불 (영수증 취소)")
def test_cash_payment_with_business_receipt_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_under_50k_with_business_receipt(BUSINESS_NUMBER)
    RefundFlow(driver_at_appium_category).refund_with_business_receipt(BUSINESS_NUMBER)
