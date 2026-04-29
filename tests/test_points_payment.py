import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

PHONE_LAST4 = "7745"
POINTS = "1000"


@allure.feature("포인트 결제")
@allure.story("포인트 카드 결제 → 환불")
def test_points_card_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_50k_with_points(PHONE_LAST4, POINTS)
    RefundFlow(driver_at_appium_category).refund_latest_payment()


@allure.feature("포인트 결제")
@allure.story("포인트 현금 결제 → 환불")
def test_points_cash_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_50k_with_points(PHONE_LAST4, POINTS)
    RefundFlow(driver_at_appium_category).refund_latest_payment()
