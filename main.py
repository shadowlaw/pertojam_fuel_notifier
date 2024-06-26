import sys
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import config
import logging

from error.RetryException import RetryException
from utils import retry_function

logger = logging.getLogger(__name__)

# TODO: Save new price changes to database
# TODO: Graph screenshot with price change over time period

# get fuel data
driver = None
options = webdriver.ChromeOptions()
options.headless = config.APP["SELENIUM_HEADLESS"]
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

if config.APP['SELENIUM_IS_REMOTE']:
    time.sleep(5)
    driver = webdriver.Remote(config.APP['SELENIUM_REMOTE_URL'], options=options)
else:
    CHROMEDRIVER_PATH = os.path.normpath(f'{os.getcwd()}/drivers/chrome/chromedriver')
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)


logger.info(f'Getting fuel data from {config.APP["FUEL_URL"]}')

try:
    driver.get(config.APP["FUEL_URL"])
except TimeoutException as e:
    logger.error(e.msg)
    try:
        retry_function(driver.get, retries=3, url=config.APP['FUEL_URL'])
    except RetryException as e:
        logger.critical(e.msg)
        sys.exit()
except Exception as e:
    logger.critical(f"Critical Error {e}")
    sys.exit()

logger.info(f'Successful request from {config.APP["FUEL_URL"]}')


table = None
try:
    table = driver.find_element(by=By.XPATH, value=config.APP["FUEL_TABLE_PATH"])
except NoSuchElementException as e:
    logger.critical(f"Unable to locate fuel price table using xpath {config.APP['FUEL_TABLE_PATH']}")
    sys.exit()
except Exception as e:
    logger.critical(f"{type(e).__name__}:{e}")
    driver.close()
    sys.exit()

msg = None

try:
    table_arr = table.text.split('\n')
    driver.close()

    date = table_arr[1]

    msg = f"This Week's Fuel Price Change Applied on: {date.split(':')[-1].strip()}\n\n"

    logger.info('Parsing fuel table')
    for fuel_update_row in table_arr[2:]:
        row_arr = fuel_update_row.split()
        price_change_percentage = row_arr[-1]
        price_change_value = row_arr[-2]
        current_price = row_arr[-3]
        fuel_type = f'{row_arr[0]} {row_arr[1]}' if row_arr[0] in ['Gasolene', 'Auto'] else row_arr[0]
        msg += f'Fuel Type: {fuel_type}\nNew Price: {current_price}\nPrice Change: {price_change_value} {price_change_percentage}\n\n'

    logger.info(f'Fuel data parsing successful')
except Exception as e:
    logger.critical(f"{type(e).__name__}:{e}")
    sys.exit()
msg += f'Data source: {config.APP["FUEL_URL"]}'

telegram_url = f'https://api.telegram.org/bot{config.APP["TELEGRAM_TOKEN"]}/sendMessage?chat_id={config.APP["TELEGRAM_GROUP_ID"]}&text={msg}'

logger.info(f'Sending Telegram message')
try:
    response = requests.get(telegram_url)

    response_msg = f'Telegram send message responded with: {response.status_code}'

    if 200 <= response.status_code <= 299:
        logger.info(response_msg)
    else:
        logger.error(response_msg)
        logger.error(response.text)
except Exception as e:
    logger.critical(f"{type(e).__name__}:{e}")
