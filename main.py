from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# TODO: Add config via .env file
# TODO: Add logging
# TODO: Exception handling for page timeout and table not found (send notification to admin)
# TODO: Save new price changes to database

CHROMEDRIVER_PATH = os.path.normpath(f'{os.getcwd()}/drivers/chrome/chromedriver-100.0.4896.60')

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)


driver.get("https://www.petrojam.com/")
table = driver.find_element(by=By.XPATH, value='//*[@id="wpv-view-layout-1528"]/div/div/table[1]')

table_arr = table.text.split('\n')
driver.close()

date = table_arr[1]

msg = f"This Week's Fuel Price Change Applied on {date.split(':')[-1].strip()}\n\n"

for fuel_update_row in table_arr[2:]:
    row_arr = fuel_update_row.split()
    price_change_percentage = row_arr[-1]
    price_change_value = row_arr[-2]
    current_price = row_arr[-3]
    fuel_type = f'{row_arr[0]} {row_arr[1]}' if row_arr[0] in ['Gasolene', 'Auto'] else row_arr[0]
    msg += f'Fuel Type: {fuel_type}\nCurrent Price: {current_price}\nPrice Change: {price_change_value} {price_change_percentage}\n\n'

print(msg)

