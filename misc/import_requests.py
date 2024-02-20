import requests
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from dropbox import Dropbox
from dropbox.files import WriteMode
import os
from threading import Lock

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# Dropbox access token
DROPBOX_ACCESS_TOKEN = "sl.BvpssmYBwYbPqA6V10Lg2yx8WXTNygtQAOMLan7ojLWIE0PfGhoob2r159sDGpDJsFhuA5jLt-HPJcFrJzhTlVeUqmrAbbeOSad1C2nlNf6yPCiH_clAAUtQUMec2ZoHwH2jP4y5Azdw"


def process_page_with_selenium(page_url, dbx, dropbox_folder, driver_path):
    global processed_pdfs_count  # Reference the global counter
    with lock:  # Ensure thread-safe check of the counter
        if processed_pdfs_count >= pdfs_limit:
            return  # Exit if the limit is reached

    # Initialize the WebDriver
    driver = webdriver.Chrome(executable_path=driver_path)

    try:
        driver.get(page_url)
        print(f"Processing page: {page_url}")
        
        # Wait for the button to be clickable, and then click it
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'tgp__trigger'))
            )
            button.click()
            time.sleep(2)  # Wait a bit for the content to load dynamically
        except TimeoutException:
            print("Button not found or not clickable. Skipping page.")
            return

        # After clicking, the dynamic content should be loaded
        # Now you can process this content, e.g., extract PDF links
        # This is a placeholder, you will need to adjust it based on the actual content
        # Example: Finding all links to PDFs
        pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='_PBIS']")
        for link in pdf_links:
            pdf_url = link.get_attribute('href')
            if pdf_url and processed_pdfs_count < pdfs_limit:
                with lock:
                    if processed_pdfs_count >= pdfs_limit:
                        break  # Check again due to potential race condition
                    upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder)
                    processed_pdfs_count += 1  # Increment the counter
                    print(f"Uploaded PDF {processed_pdfs_count}/{pdfs_limit}")
    finally:
        driver.quit()




# def upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder):
#     # Attempting to download PDF from URL
#     response = requests.get(pdf_url)
#     if response.status_code == 200:
#         pdf_content = response.content
#         # Attempting to parse the PDF URL to extract the title
#         try:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             title_element = soup.find('li', class_='item-type-ld').find('a', href=True)
#             if title_element:
#                 # Extracting title from the title element
#                 title = os.path.splitext(os.path.basename(title_element['href']))[0]
#                 print(f"Attempting to upload {title}.pdf to Dropbox...")
#                 pdf_path = f"/{dropbox_folder}/{title}.pdf"
#                 # Uploading the PDF content to Dropbox
#                 try:
#                     dbx.files_upload(pdf_content, pdf_path, mode=WriteMode("overwrite"))
#                     print(f"Successfully uploaded {title}.pdf to Dropbox.")
#                 except Exception as e:
#                     print(f"Error uploading file: {e}")
#             else:
#                 print("Title element not found. Skipping upload.")
#         except Exception as e:
#             print(f"Error processing PDF URL {pdf_url}: {e}")
#     else:
#         print(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")


def upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder):
    # Check if the URL contains '_PBIS'
    if '_PBIS' in pdf_url:
        print(f"Attempting to download PDF from URL: {pdf_url}")
        response = requests.get(pdf_url)
        if response.status_code == 200:
            pdf_content = response.content
            # Extracting the PDF filename from the URL
            pdf_filename = pdf_url.split('/')[-1]
            # Optional: Remove URL encoding or unwanted characters if necessary
            title = os.path.splitext(pdf_filename)[0]
            print(f"Attempting to upload {title}.pdf to Dropbox...")
            pdf_path = f"/{dropbox_folder}/{title}.pdf"
            try:
                dbx.files_upload(pdf_content, pdf_path, mode=WriteMode("overwrite"))
                print(f"Successfully uploaded {title}.pdf to Dropbox.")
            except Exception as e:
                print(f"Error uploading file: {e}")
        else:
            print(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")
    else:
        print(f"URL does not contain '_PBIS'. Skipping: {pdf_url}")


# # Upload PDF to Dropbox
# def upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder):
#     print(f"Attempting to upload {title}.pdf to Dropbox...")
#     response = requests.get(pdf_url)
#     if response.status_code == 200:
#         pdf_content = response.content
#         soup = BeautifulSoup(response.text, 'html.parser')
#         title_element = soup.find('li', class_='item-type-ld').find('a', href=True)
#         if title_element:
#             title = os.path.splitext(os.path.basename(title_element['title']))[0]
#             pdf_path = f"/{dropbox_folder}/{title}.pdf"
#             dbx.files_upload(pdf_content, pdf_path, mode=WriteMode("overwrite"))
#             print(f"Successfully uploaded {title}.pdf to Dropbox.")
#             print(f"Uploaded: {title}.pdf to Dropbox")


# Initialize a lock
lock = Lock()

# Initialize the counter and limit as before
processed_pdfs_count = 0
pdfs_limit = 20  # Or any small number you want to test with

def process_page(page_url, dbx, dropbox_folder):
    global processed_pdfs_count  # Reference the global counter
    with lock:  # Ensure thread-safe increment/check of the counter
        if processed_pdfs_count >= pdfs_limit:
            return  # Exit if the limit is reached

    response = requests.get(page_url)
    if response.status_code == 200:
        print(f"Processing page: {page_url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        for know_more_div in soup.find_all('div', class_='know-more'):
            with lock:  # Check and increment within a locked context to ensure thread safety
                if processed_pdfs_count >= pdfs_limit:
                    return  # Exit if the limit is reached
            keywords = know_more_div.find('p', class_='decision__motcles')
            if keywords and 'générique' in keywords.text:
                pdf_link_element = know_more_div.find('li', class_='item-type-ld').find('a', href=True)
                if pdf_link_element:
                    pdf_url = pdf_link_element['href']
                    with lock:
                        # Check again to avoid a race condition where the limit is reached while processing
                        if processed_pdfs_count >= pdfs_limit:
                            return
                        processed_pdfs_count += 1  # Increment the counter
                    upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder)
                    print(f"Uploaded PDF {processed_pdfs_count}/{pdfs_limit}")



# # Global counter for processed PDFs
# processed_pdfs_count = 0
# pdfs_limit = 5  # Limit to the number of PDFs to process for testing

# def process_page(page_url, dbx, dropbox_folder):
#     global processed_pdfs_count  # Reference the global counter
#     if processed_pdfs_count >= pdfs_limit:
#         return  # Stop processing if the limit is reached
    
#     response = requests.get(page_url)
#     if response.status_code == 200:
#         print(f"Processing page: {page_url}")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for know_more_div in soup.find_all('div', class_='know-more'):
#             if processed_pdfs_count >= pdfs_limit:
#                 break  # Stop the loop if the limit is reached
#             keywords = know_more_div.find('p', class_='decision__motcles')
#             if keywords and 'générique' in keywords.text:
#                 pdf_link_element = know_more_div.find('li', class_='item-type-ld').find('a', href=True)
#                 if pdf_link_element:
#                     pdf_url = pdf_link_element['href']
#                     upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder)
#                     processed_pdfs_count += 1  # Increment the counter after a successful process


# #Process a single page
# def process_page(page_url, dbx, dropbox_folder):
#     response = requests.get(page_url)
#     if response.status_code == 200:
#         print(f"Processing page: {page_url}")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for know_more_div in soup.find_all('div', class_='know-more'):
#             keywords = know_more_div.find('p', class_='decision__motcles')
#             if keywords and 'générique' in keywords.text:
#                 pdf_link_element = know_more_div.find('li', class_='item-type-ld').find('a', href=True)
#                 if pdf_link_element:
#                     pdf_url = pdf_link_element['href']
#                     upload_pdf_to_dropbox(pdf_url, dbx, dropbox_folder)

#Run the script concurrently
def run_concurrent_requests(start_page, end_page, dbx, dropbox_folder):
    page_urls = [f'https://www.anses.fr/fr/decisions?page={page}' for page in range(start_page, end_page + 1)]
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: process_page(url, dbx, dropbox_folder), page_urls)

# Main script
if __name__ == "__main__":
    start_page = 1  #starting page number
    end_page = 2368  #ending page number

    # Dropbox folder name
    dropbox_folder = "Apps/ANSES v2"

    # Create Dropbox instance
    dbx = Dropbox(DROPBOX_ACCESS_TOKEN)

    # Run concurrent requests
    print(f"Scraping pages {start_page} to {end_page}...")
    run_concurrent_requests(start_page, end_page, dbx, dropbox_folder)

    print("Script completed.")
