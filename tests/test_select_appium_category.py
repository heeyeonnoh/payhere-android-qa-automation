from ..driver.appium_driver import create_android_driver
from ..pages.product_page import ProductPage

def test_select_appium_category():
    driver = create_android_driver()
    page = ProductPage(driver)

    page.go_to_product_tab()
    page.select_appium_category()
