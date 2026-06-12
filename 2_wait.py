"""Example: demonstrate implicit + explicit waits with Selenium.

This module is PEP8-compliant and structured for reuse and testing.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_driver() -> webdriver.Chrome:
    """Create and return a Chrome WebDriver with sensible defaults.

    The implicit wait is set once here so callers do not need to manage it.
    """
    options = webdriver.ChromeOptions()
    # Uncomment the next line to run in headless mode if desired.
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def click_submit_button(driver: webdriver.Chrome, url: str) -> None:
    """Navigate to ``url`` and click the submit button when clickable.

    Uses an explicit wait for precision control.
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    submit_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-form"))
    )
    submit_btn.click()


def main() -> None:
    """Entry point for the module."""
    driver = create_driver()
    try:
        click_submit_button(driver, "https://jsonplaceholder.typicode.com/")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()