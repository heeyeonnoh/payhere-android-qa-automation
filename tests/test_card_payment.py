from driver.appium_driver import create_android_driver
from flows.product_flow import ProductFlow
from flows.payment_flow import PaymentFlow


def test_card_payment_under_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).card_under_50k()


def test_card_payment_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).card_50k()


def test_card_payment_over_50k():
    driver = create_android_driver()
    ProductFlow(driver).go_to_appium_category()
    PaymentFlow(driver).card_over_50k()
