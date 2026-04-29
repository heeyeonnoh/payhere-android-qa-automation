import allure
from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow

QTY = "5"


@allure.feature("단위 상품 결제")
@allure.story("단위 카드 결제 → 환불")
def test_unit_card_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_unit(QTY)
    RefundFlow(driver_at_appium_category).refund_latest_payment()


@allure.feature("단위 상품 결제")
@allure.story("단위 현금 결제 → 환불")
def test_unit_cash_payment_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_unit(QTY)
    RefundFlow(driver_at_appium_category).refund_latest_payment()
