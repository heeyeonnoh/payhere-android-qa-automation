from pages.product_page import ProductPage


def test_select_appium_category(driver):
    page = ProductPage(driver)
    page.go_to_product_tab()
    page.select_appium_category()
