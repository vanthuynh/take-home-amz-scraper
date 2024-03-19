import time
import json
import os
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from amazoncaptcha import AmazonCaptcha
from product import Product

LOG_FILE = "res.json"
CSV_FILE = "DATA.csv"
SEND_MAIL = True
KEEP_TRACKING = True

class AmazonProductScraper:
    def __init__(self):
        self.driver = None
        self.repeat_time = 30      # repeat time will be 5 minutes

    def open_browser(self):
        options = Options()
        options.headless = True

        # Provide the path to Chromedriver
        chromedriver_path = '/chromedriver'

        # Configure Chrome WebDriver with options
        self.driver = webdriver.Chrome(options=options)

        # Navigate to Amazon website
        url = "https://www.amazon.com/"
        self.driver.get(url)
        time.sleep(2) # Wait for 2 seconds for the page to fully load

        ### Begin solving captcha challenge
        link = self.driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')
        captcha = AmazonCaptcha.fromlink(link)
        captcha_value = AmazonCaptcha.solve(captcha)
        input_field = self.driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        button = self.driver.find_element(By.CLASS_NAME, "a-button-text")
        button.click()

        time.sleep(5)  # Wait for 5 seconds for the page to fully load

    def scrape_product_details(self, url):
        products = []
        most_recent_price = float('inf')
        refresh_once = False
        product_titles, price_dollar, price_cent = None, None, None
        while KEEP_TRACKING:
            if refresh_once == False:
                self.driver.get(url)
                refresh_once = True
            else:
                self.driver.refresh()
            try:
                # Wait for the elements to be present before proceeding
                wait = WebDriverWait(self.driver, 20)
                product_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-large product-title-word-break']")))
                price_dollar = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-whole']")))
                price_cent = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-fraction']")))
                print("Product elements found successfully.")
            except TimeoutException as e:
                print(f"Error finding product elements: {e}")
                break

            for title, dollar, cent in zip(product_titles, price_dollar, price_cent):
                try:
                    title_text = title.text
                    if dollar != '' and cent != '':
                        price_text = '.'.join([dollar.text, cent.text])
                    else:
                        price_text = 0

                    # compare previous price
                    most_recent_price = min(float(price_text), most_recent_price)
                    print(most_recent_price)

                    time_scraped = datetime.now()

                    product = Product(title_text, price_text, time_scraped)
                    products.append(product)
                except Exception as ex:
                    print(f"Error occurred while extracting product information: {ex}")
                    continue

            # Save products to JSON file
            self.save_to_json(products)

            # Update CSV file
            self.save_to_csv(products)

            ### Wait for certain minutes before reloading page
            time.sleep(self.repeat_time)

        # return products
        return products

    def save_to_json(self, products):
        # file_name = f"{query.replace(' ', '_')}.json"
        with open(LOG_FILE, "w") as f:
            json.dump([{'title': product.title, 'price': product.price, 'scraping_timestamp': str(product.scraping_timestamp)} for product in products], f)
        print(f"Products scraped have been saved to '{LOG_FILE}'")

    def save_to_csv(self, products):
        # file_name = f"{query.replace(' ', '_')}.json"
        df = pd.DataFrame(
        {
            "Title": [products[-1].title],
            "Price": [products[-1].price]
            # "Dimensions": dimensions
        })
        df.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.exists(CSV_FILE))
        print(f"Products scraped have been saved to '{CSV_FILE}'")

    def close_browser(self):
        self.driver.quit()
