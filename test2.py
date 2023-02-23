import random
import requests
import pandas as pd
import time
import re
import logging
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.INFO)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--headless')

options.add_argument('log-level=3')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
#driver = webdriver.Chrome(
   # options=options, executable_path=r"/Users/xxxxxx/Desktop/chromedriver_mac_arm64/chromedriver")

# URLs to scrape
urls = ["https://www.ubuy.com.py/en/search/?q=syngenta",
        "https://www.ubuy.cl/en/search/?q=syngenta"]

for url in urls:
    # Get scroll height
    driver.get(url)
    time.sleep(random.randint(10, 100))

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Wait for lazy loading
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product")))

    name_list = []
    url_list = []
    price_list = []
    seller_list = []

    # FINDALL
    try:
        for i in soup.find_all("div", {"class": "product"}):

            # NAME
            try:
                name = i.find(
                    "h2", {"class": "product-title"}).text  # .strip()
                print(name)
                name_list.append(name)
            except Exception as e:
                logging.critical(f'Unable to parse product name, error: {e}')

            # URL
            try:
                url = i.find(
                    "a", {"class": "img-detail goos-tag-product"})['href']
                url_list.append(url)
            except Exception as e:
                logging.critical(f'Unable to parse product url, error: {e}')

            # PRICE
            try:
                price = i.find(
                    "h3", {"class": "product-price"}).text
                price = re.sub("[^0-9,]", "", price)
            except:
                price = "N/A"
            price_list.append(price)
            print(name, url, name)
        pd_dict = {'name': name_list, 'url': url_list, 'price': price_list}
        df = pd.DataFrame(pd_dict)
        df['country'] = 'PARAGUAY' if 'ubuy.com.py/en/' in url else 'CHILE'
        df['region'] = 'LATAM'
        df['domain'] = url
        df['seller'] = "ubuy"

        print(df)

    except Exception as e:
        logging.critical(f'Unable to parse product listings, error: {e}')

now = datetime.now()
date_now = now.strftime('%Y-%m-%d')
text = "ubuy"
# path = f"\\C:\\Splunk\\online\\parsehub\\{text}_{date_now}.csv"
# df
