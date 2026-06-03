from selenium import webdriver
from selenium.webdriver.common.by import By
# Advanced wait modules
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# --- TECHNIQUE A: IMPLICIT WAIT (Global rule) ---
driver.implicitly_wait(5) # Globally wait up to 5 seconds for everything

driver.get("https://jsonplaceholder.typicode.com/")

# --- TECHNIQUE B: EXPLICIT WAIT (Precision control) ---
# Wait up to 10 seconds specifically for an element to become clickable
wait = WebDriverWait(driver, 10)
submit_btn = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-form"))
)
submit_btn.click()