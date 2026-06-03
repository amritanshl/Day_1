# 1. Import the specific modules we need
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Allows us to hit keyboard buttons like Enter


print("Initializing robot browser...")

# 2. Fire up a brand-new, isolated instance of Google Chrome
driver = webdriver.Chrome()

# 3. Tell our automated browser to visit a webpage
driver.get("https://acme-test.uipath.com/")

# Print out the webpage's title to verify we are there
print(f"Successfully reached: {driver.title}")

my_email = driver.find_element(By.ID, "email")
my_email.send_keys("amritanshlal@gmail.com")

# 4. Leave the browser open for 5 seconds so we can look at it, then close it
import time
time.sleep(5)
driver.quit()