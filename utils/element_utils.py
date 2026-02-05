from selenium.common.exceptions import TimeoutException
from .wait_utils import wait_for_presence


def is_element_present(driver, locator, timeout=3):
    try:
        wait_for_presence(driver, locator, timeout)
        return True
    except TimeoutException:
        return False
