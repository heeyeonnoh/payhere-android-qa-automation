import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow


@allure.feature("분할 결제")
@allure.story("분할 결제 (현금 → 카드) → 환불")
def test_split_cash_card_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).split_cash_card()
    RefundFlow(driver_at_appium_category).refund_split_dutch_payments()


@allure.feature("분할 결제")
@allure.story("분할 결제 (카드 → 카드) → 환불")
def test_split_card_card_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).split_card_card()
    RefundFlow(driver_at_appium_category).refund_split_dutch_payments()
