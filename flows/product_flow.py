from pages.product_page import ProductPage


class ProductFlow:
    def __init__(self, driver):
        self.page = ProductPage(driver)

    def go_to_appium_category(self):
        self.page.go_to_product_tab()
        self.page.select_appium_category()

