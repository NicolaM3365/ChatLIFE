from selenium import webdriver

# Specify the correct path to your ChromeDriver
driver_path = 'C:/Users/Nicola.Mitchell/chromedriver-win64/chromedriver.exe'

driver = webdriver.Chrome(executable_path=driver_path)

# Example: Open Google
driver.get("https://www.google.com/")

# Add your automation script here

# Don't forget to close the browser when you're done
driver.quit()


