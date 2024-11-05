import os
from urllib.request import urlretrieve
import requests


import os
from urllib.request import urlretrieve
import backoff
import urllib.error

@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    (urllib.error.URLError, ConnectionResetError),  # Errors to retry on
    max_tries=5  # Maximum number of retries
)
def download_image(image_url, image_path):
    urlretrieve(image_url, image_path)

def save_images(product_id, website_name, images):
    folder_name = f"images/{website_name}/{product_id}"
    os.makedirs(folder_name, exist_ok=True)
    if os.listdir(folder_name):
        return None
    for idx, image_url in enumerate(images):
        
        if image_url:
            image_path = os.path.join(folder_name, f"image_{idx + 1}.jpg")
            try:
                download_image(image_url, image_path)
            except Exception as e:
                print(f"Failed to download {image_url}: {e}")
    
    return folder_name



def is_shopify_site(url):
    # Normalize URL
    url = url.rstrip("/")

    # Check for the /products.json endpoint
    json_url = f"{url}/products.json"
    try:
        response = requests.get(json_url, timeout=5)
        if response.status_code == 200 and "products" in response.json():
            return True
    except:
        pass

    # Check for Shopify CDN in the HTML source
    try:
        response = requests.get(url, timeout=5)
        if "cdn.shopify.com" in response.text:
            return True
    except:
        pass

    return False


def check_platform(url):
    if is_shopify_site(url):
        return "Shopify"
    # Placeholder for additional platform checks (e.g., BigCommerce, Wix)
    # elif is_bigcommerce_site(url):
    #     return "BigCommerce"
    # elif is_wix_site(url):
    #     return "Wix"
    else:
        return "Unknown"
