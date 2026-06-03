import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Allows us to hit keyboard buttons like Enter

# 1. Initialize our Chrome automation engine
driver = webdriver.Chrome()

try:
    # 2. Go to the main Wikipedia portal
    driver.get("https://www.wikipedia.org")
    
    # 3. LOCATE the search bar element using its HTML ID attribute
    # Wikipedia's search input has the id="searchInput"
    search_bar = driver.find_element(By.ID, "searchInput")
    
    print("Found the search bar! Typing query...")
    
    # 4. ACT: Type a query into the field and append the ENTER key press
    search_bar.send_keys("Python (programming language)" + Keys.ENTER)
    
    # Wait 3 seconds for the dynamic search results page to load
    time.sleep(3)
    
    # 5. VERIFY: Grab the new page header element using its Class Name
    # Wikipedia page titles use class="mw-page-title-main"
    page_header = driver.find_element(By.CLASS_NAME, "mw-page-title-main")
    
    print(f"Success! Arrived at page header: '{page_header.text}'")

finally:
    # Always clean up and shutdown the browser session safely
    driver.quit()