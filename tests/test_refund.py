from flows.payment_flow import PaymentFlow
from flows.refund_flow import RefundFlow


def test_card_payment_under_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_under_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment()


def test_card_payment_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment_50k()


def test_card_payment_over_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_over_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment_over_50k()


def test_cash_payment_under_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_under_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment()


def test_cash_payment_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment()


def test_cash_payment_over_50k_and_refund(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_over_50k()
    RefundFlow(driver_at_appium_category).refund_latest_payment()
