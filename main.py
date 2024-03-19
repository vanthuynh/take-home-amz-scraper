import time
import json
from selenium.common.exceptions import TimeoutException
from amazon_scraper import AmazonProductScraper
from query_reader import read_queries

def main():
    scraper = AmazonProductScraper()
    scraper.open_browser()
    product_url = "https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9FPHY6"
    try:
        scraper.scrape_product_details(product_url)
    except TimeoutException:
        print(f"TimeoutException occurred. ")

    scraper.close_browser()

if __name__ == "__main__":
    main()
