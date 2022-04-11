from distutils.util import strtobool
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Add logging
# TODO: Exception handling for page timeout and table not found (send notification to admin)
# TODO: Save new price changes to database
# TODO: Graph screenshot with price change over time period

# get fuel data
CHROMEDRIVER_PATH = os.path.normpath(f'{os.getcwd()}/drivers/chrome/{os.getenv("SELENIUM_CHROME_DRIVER")}')

options = webdriver.ChromeOptions()
options.headless = bool(strtobool(os.getenv("SELENIUM_HEADLESS")))
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)


driver.get(os.getenv("FUEL_URL"))
table = driver.find_element(by=By.XPATH, value=os.getenv("FUEL_TABLE_PATH"))

table_arr = table.text.split('\n')
driver.close()

date = table_arr[1]

msg = f"This Week's Fuel Price Change Applied on: {date.split(':')[-1].strip()}\n\n"

for fuel_update_row in table_arr[2:]:
    row_arr = fuel_update_row.split()
    price_change_percentage = row_arr[-1]
    price_change_value = row_arr[-2]
    current_price = row_arr[-3]
    fuel_type = f'{row_arr[0]} {row_arr[1]}' if row_arr[0] in ['Gasolene', 'Auto'] else row_arr[0]
    msg += f'Fuel Type: {fuel_type}\nCurrent Price: {current_price}\nPrice Change: {price_change_value} {price_change_percentage}\n\n'

msg += f'data source {os.getenv("FUEL_URL")}'
# send Telegram message

telegram_url = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/sendMessage?chat_id={os.getenv("TELEGRAM_GROUP_ID")}&text={msg}'

response = requests.get(telegram_url)
print(f'Telegram send message{response.status_code}')
