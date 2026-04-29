import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

PRICE = "2000"


@allure.feature("시가 상품 결제")
@allure.story("시가 카드 결제 → 환불")
def test_market_price_card_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_market_price(PRICE)
    RefundFlow(driver_at_appium_category).refund_latest_payment()


@allure.feature("시가 상품 결제")
@allure.story("시가 현금 결제 → 환불")
def test_market_price_cash_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_market_price(PRICE)
    RefundFlow(driver_at_appium_category).refund_latest_payment()
