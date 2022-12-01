from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
import time
from datetime import datetime
from datetime import timedelta
import json
from binance.client import Client

binance_api_key = 'X5ToDORXBgYkW2g0uAfeau3j53StPKUA0BVyc2c1LDjlijh87Jp3HTOA7nlr60kP'
binance_api_secret = 'xtSC014vOjmFRFADIXpv4NscjKFb34OFGtzncHqMSR8amNfpiRkI8tpR0cdQahx5'

client = Client(binance_api_key, binance_api_secret)

# Screen shot
def save_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png') -> None:
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(path)  # has scrollbar

tele_token = '1914822073:AAGY3gT842M9vS3_-6V37gwiDeQa6mu_VzU'
chat_id = '943105950'

options = Options()
options.headless = True
options.add_argument("--window-size=2316,1080")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    options=options) #, executable_path='/samsung/chromedriver'

driver.get("https://www.binance.com/")
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "header_login")))
driver.find_element(By.ID, "header_login").click()
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap_app"]/main/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]')))
element = driver.find_element(By.XPATH, '//*[@id="wrap_app"]/main/div[2]/div/div[2]/div[2]/div[2]/div[1]')
element.screenshot('QR.png')
# save_screenshot(driver,"binance.png")
telegram_notify = telegram.Bot(tele_token)
telegram_notify.send_photo(chat_id=chat_id, photo=open('QR.png', 'rb'))
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "header_menu_cabinet")))
save_screenshot(driver,"binance.png")
while True:
	time.sleep(1)