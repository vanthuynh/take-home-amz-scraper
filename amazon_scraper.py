import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
from product import Product


class AmazonProductScraper:
    def __init__(self):
        self.driver = None

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
        time.sleep(5)  # Wait for 5 seconds for the page to fully load

    def scrape_product_details(self, query, num_pages=1):
        products = []

        for page in range(1, num_pages + 1):
            self.driver.get(f"https://www.amazon.com/s?k={query.replace(' ', '+')}&page={page}")

            try:
                # Wait for the elements to be present before proceeding
                wait = WebDriverWait(self.driver, 10)
                product_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))
                product_prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-whole']")))
                product_ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-icon-alt']")))
                product_asin = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-result-item s-asin')]")))
                # product_asin = self.driver.find_elements(By.XPATH, "//img[@class='s-image']")
                print("Product elements found successfully.")
            except TimeoutException as e:
                print(f"Error finding product elements: {e}")
                continue

            for title, price, rating, image in zip(product_titles, product_prices, product_ratings, product_asin):
                try:
                    title_text = title.text
                    price_text = price.text
                    rating_text = rating.get_attribute("innerHTML")
                    asin = image.get_attribute("data-asin")

                    product = Product(title_text, price_text, asin, rating_text, datetime.now())
                    products.append(product)
                except Exception as ex:
                    print(f"Error occurred while extracting product information: {ex}")
                    continue

        # Save products to JSON file
        self.save_to_json(products, query)

        return products

    def save_to_json(self, products, query):
        file_name = f"{query.replace(' ', '_')}.json"
        with open(file_name, "w") as f:
            json.dump([{'title': product.title, 'price': product.price, 'asin': product.asin, 'rating': product.rating, 'scraping_timestamp': str(product.scraping_timestamp)} for product in products], f)

        print(f"Products scraped for '{query}' have been saved to '{file_name}'")

    def close_browser(self):
        self.driver.quit()
