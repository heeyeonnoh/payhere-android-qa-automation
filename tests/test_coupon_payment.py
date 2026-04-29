import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

PHONE_LAST4 = "7745"


@allure.feature("쿠폰 결제")
@allure.story("쿠폰 카드 결제 → 환불")
def test_coupon_card_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_50k_with_coupon(PHONE_LAST4)
    RefundFlow(driver_at_appium_category).refund_latest_payment()


@allure.feature("쿠폰 결제")
@allure.story("쿠폰 현금 결제 → 환불")
def test_coupon_cash_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_50k_with_coupon(PHONE_LAST4)
    RefundFlow(driver_at_appium_category).refund_latest_payment()
