# shopify_scraper/scraper.py
import requests
from utils.utils import save_images
import re, json
from bs4 import BeautifulSoup


def extract_description(html_data):
    # Remove control characters
    clean_data = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', html_data)
    # Use BeautifulSoup to parse the HTML directly
    soup = BeautifulSoup(clean_data, 'html.parser')
    # Get the text from the parsed HTML, cleaning up the content
    description = soup.get_text(separator=' ', strip=True)
    return description


def fetch_product_data(url):
    print(f"fetching products details for {url}")
    page = 1
    products = []
    while True:
        response = requests.get(f"{url}/products.json?limit=250&page={page}", timeout=5)
        response.raise_for_status()
        products_data = response.json().get("products", [])
        print(f"count of product data for page {page} is {len(products_data)}")
        if not products_data:
            print("breaking since no product data found")
            break
        products.extend(products_data)
        print(f"Total product count after extending : {len(products)}")
        page += 1

    return products
        


def scrape_website(url, website_name, insert_data_func):
        products = fetch_product_data(url)
        print(f"{website_name} : {len(products)}")

        for product in products:
            images = product.get("images", [])
            image_folder = save_images(product["id"], website_name, images)

            product_data = {
                "website_name" : website_name,
                "website_url" : url,
                "product_url" : f"{url}/products/{product['handle']}",
                "product_id" : product["id"],
                "product_title" : product.get("title"),
                "product_description" : extract_description(product.get("body_html")),
                "price" : float(product["variants"][0].get("price", 0)),
                "vendor" : product.get("vendor"),
                "product_type" : product.get("product_type"),
                "tags" : ", ".join(product.get("tags", [])),
                "image_folder" : image_folder
            }
            insert_data_func(product_data, image_folder)