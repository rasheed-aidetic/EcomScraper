# shopify_scraper/scraper.py
import requests
from utils.utils import save_images


def fetch_product_data(url, page=1):
    response = requests.get(f"{url}/products.json?limit=250&page={page}", timeout=5)
    response.raise_for_status()
    return response.json().get("products", [])


def scrape_website(url, insert_data_func):
    page = 1
    while True:
        products = fetch_product_data(url, page=page)
        if not products:
            break
        for product in products:
            images = product.get("images", [])
            image_folder = save_images(product["id"], images)
            insert_data_func(product, image_folder)
        page += 1
