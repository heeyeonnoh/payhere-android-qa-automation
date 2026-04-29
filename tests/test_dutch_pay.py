import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow


@allure.feature("더치페이")
@allure.story("더치페이 2명 (현금 → 카드) → 환불")
def test_dutch_pay_cash_card_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).dutch_pay_cash_card()
    RefundFlow(driver_at_appium_category).refund_latest_payment()
