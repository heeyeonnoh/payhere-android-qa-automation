from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow


def test_card_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_under_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment()
