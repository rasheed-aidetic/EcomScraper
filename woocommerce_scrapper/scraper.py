# shopify_scraper/scraper.py
import requests
from utils.utils import save_images
import re, json
from bs4 import BeautifulSoup



def fetch_product_data(url):
    print(f"fetching products details for {url}")
    page = 1
    products = []
    while page < 2:
        response = requests.get(f"{url}/wp-json/wp/v2/product?limit=10&page={page}", timeout=15)
        try:
            response.raise_for_status()
        except:
            import traceback
            traceback.print_exc()
            break
        products_data = response.json()
        print(f"count of product data for page {page} is {len(products_data)}")
        if not products_data:
            print("breaking since no product data found")
            break
        products.extend(products_data)
        print(f"Total product count after extending : {len(products)}")
        page += 1

    return products

def scrap_and_extract_images_from_shyle(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    
    # Send request to the product page
    response = requests.get(product_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract product details
    product_data = {}
    
    # Images
    product_data['images'] = []
    gallery = soup.find_all("div", class_="woocommerce-product-gallery__image")
    for item in gallery:
        img = item.find("img")
        if img and 'data-large_image' in img.attrs:
            product_data['images'].append(img['data-large_image'])  # Full resolution image
        elif img and 'src' in img.attrs:
            product_data['images'].append(img['src'])  # Thumbnail or other size
    
    return product_data
        


def scrape_website(url, website_name, insert_data_func):
        products = fetch_product_data(url)
        print(f"{website_name} : {len(products)}")

        for product in products:
            print(f"Fetching product data for {website_name} : {product.get('id')}")
            images = scrap_and_extract_images_from_shyle(product.get("link"))
            image_folder = save_images(product["id"], website_name, images.get("images"))
            if not image_folder:
                print("Image Folder already exists. Skipping !!!!!!!!!!!!!")
                continue
            product_data = {
                "website_name" : website_name,
                "website_url" : url,
                "product_url" : product.get("yoast_head_json").get("og_url"),
                "product_id" : product.get("id"),
                "product_title" : product.get("yoast_head_json").get("title"),
                "product_description" : product.get("yoast_head_json").get("og_title"),
                "price" : 0,
                "vendor" : website_name,
                "product_type" : product.get("product_type", ""),
                "tags" : ", ".join(product.get("tags", [])),
                "image_folder" : image_folder
            }
            insert_data_func(product_data, image_folder)