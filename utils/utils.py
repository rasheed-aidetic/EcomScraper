import os
from urllib.request import urlretrieve
import requests


def save_images(product_id, images):
    folder_name = f"images/{product_id}"
    os.makedirs(folder_name, exist_ok=True)
    for idx, image in enumerate(images):
        image_url = image.get("src")
        if image_url:
            image_path = os.path.join(folder_name, f"image_{idx + 1}.jpg")
            urlretrieve(image_url, image_path)
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
