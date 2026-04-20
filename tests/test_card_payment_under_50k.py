from flows.payment_flow import PaymentFlow


def test_card_payment_under_50k(driver_at_appium_category):
    PaymentFlow(driver_at_appium_category).card_payment_under_50k()
