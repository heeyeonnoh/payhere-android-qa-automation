from ..driver.appium_driver import create_android_driver
from ..flows.product_flow import ProductFlow
from ..flows.payment_flow import PaymentFlow


def test_cash_payment_under_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).cash_under_50k()


def test_cash_payment_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).cash_50k()


def test_cash_payment_over_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).cash_over_50k()
