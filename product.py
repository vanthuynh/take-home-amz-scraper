# product/product.py

class Product:
    def __init__(self, title, price, asin, rating, scraping_timestamp):
        self.title = title
        self.price = price
        self.asin = asin
        self.rating = rating
        self.scraping_timestamp = scraping_timestamp
