import time
import json
from selenium.common.exceptions import TimeoutException
from amazon_scraper import AmazonProductScraper
from query_reader import read_queries

def main():
    scraper = AmazonProductScraper()
    scraper.open_browser()

    queries = read_queries("user_queries.json")
    for query in queries:
        try:
            scraper.scrape_product_details(query)
        except TimeoutException:
            print(f"TimeoutException occurred for query '{query}'. Moving to the next query.")
            continue

    scraper.close_browser()

if __name__ == "__main__":
    main()
