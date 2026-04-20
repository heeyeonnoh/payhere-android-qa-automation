from pages.product_page import ProductPage


class ProductFlow:
    def __init__(self, driver):
        self.page = ProductPage(driver)

    def go_to_product_tab(self):
        """상품 탭으로 이동"""
        self.page.go_to_product_tab()

    def go_to_appium_category(self):
        """상품 탭 > appium 카테고리로 이동"""
        self.page.go_to_product_tab()
        self.page.select_appium_category()
