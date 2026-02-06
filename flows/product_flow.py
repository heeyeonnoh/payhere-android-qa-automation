# flows/product_flow.py

from pages.product_page import ProductPage


def go_to_appium_category(driver):

    product_page = ProductPage(driver)

    product_page.go_to_product_tab()
    product_page.select_appium_category()
