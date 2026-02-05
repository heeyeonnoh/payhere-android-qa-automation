import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from driver.appium_driver import create_android_driver


def test_attached_app():
    driver = create_android_driver()

    print("ATTACHED OK")
    print("PACKAGE:", driver.current_package)
    print("ACTIVITY:", driver.current_activity)

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    test_attached_app()
