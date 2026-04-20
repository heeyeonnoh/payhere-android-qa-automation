from flows.payment_flow import PaymentFlow


def test_cash_payment_under_50k(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_under_50k()


def test_cash_payment_50k(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_50k()


def test_cash_payment_over_50k(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).cash_over_50k()
