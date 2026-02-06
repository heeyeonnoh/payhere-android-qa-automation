from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_utils import wait_for_visible


class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    PRODUCT_TAB = (
        AppiumBy.ACCESSIBILITY_ID,
        "상품"
    )

    APPIUM_CATEGORY = (
        AppiumBy.ACCESSIBILITY_ID,
        "appium"
    )

    def go_to_product_tab(self):
        wait_for_visible(self.driver, *self.PRODUCT_TAB).click()

    def select_appium_category(self):
        wait_for_visible(self.driver, *self.APPIUM_CATEGORY).click()
