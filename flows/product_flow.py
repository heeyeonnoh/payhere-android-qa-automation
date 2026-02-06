from ..pages.product_page import ProductPage


class ProductFlow:
    def __init__(self, driver):
        self.driver = driver
        self.product_page = ProductPage(driver)

    def go_to_appium_category(self):

        self.product_page.go_to_product_tab()
        self.product_page.select_appium_category()
