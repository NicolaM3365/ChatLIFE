

from dropbox import Dropbox
from dropbox.files import WriteMode
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

DROPBOX_ACCESS_TOKEN = "sl.BvpssmYBwYbPqA6V10Lg2yx8WXTNygtQAOMLan7ojLWIE0PfGhoob2r159sDGpDJsFhuA5jLt-HPJcFrJzhTlVeUqmrAbbeOSad1C2nlNf6yPCiH_clAAUtQUMec2ZoHwH2jP4y5Azdw"

driver_path ='C:/Users/Nicola.Mitchell/chromedriver-win64/chromedriver.exe'
# Setup WebDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Example: Open Google
# driver.get("https://www.google.com/")

driver.get("https://www.anses.fr/fr/decisions?")

# Find all PDF links that contain 'PBIS' in the URL
pbis_pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='PBIS']")

for link in pbis_pdf_links:
    # For each link, find the closest container that includes both the link and the button
    container = link.find_element(By.XPATH, "./ancestor::div[contains(@class, 'layout__item')]")

    # Within this container, find the button to click
    button = container.find_element(By.CSS_SELECTOR, "button.see-more.tgp__trigger")

    # Click the button to reveal additional content
    button.click()

    # Wait for any dynamic content to load or directly proceed with further actions
    # For example, extracting the now-visible content or URLs
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tgp__panel--is-opened"))
    )

    # Add logic here to handle the revealed content, such as extracting additional PDF links or details

# Remember to close the WebDriver session when done
driver.quit()
