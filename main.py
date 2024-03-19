import time
import json
from selenium.common.exceptions import TimeoutException
from amazon_scraper import AmazonProductScraper

def main():
    scraper = AmazonProductScraper()
    scraper.open_browser()

    # retrieve target product url (can be ask from user input)
    ### URL's preferred format is https://www.amazon.com/dp/###########
    product_url = "https://www.amazon.com/dp/B09V3JJT5D"

    try:
        scraper.scrape_product_details(product_url)
    except TimeoutException:
        print(f"TimeoutException occurred. ")

    scraper.close_browser()

if __name__ == "__main__":
    main()
