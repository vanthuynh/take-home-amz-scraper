import os
import json

def save_to_json(products, query):
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Define the directory where data will be saved
    data_directory = os.path.join(script_directory, 'data')

    # Create the data directory if it doesn't exist
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    file_name = os.path.join(data_directory, f"{query.replace(' ', '_')}.json")
    with open(file_name, "w") as f:
        json.dump([{'title': product.title, 'price': product.price, 'rating': product.rating, 'scraping_timestamp': str(product.scraping_timestamp)} for product in products], f)

    print(f"Products scraped for '{query}' have been saved to '{file_name}'")
