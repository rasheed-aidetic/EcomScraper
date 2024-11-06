import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from utils.utils import save_images
import random
import sqlite3
import config
import hashlib


def scrape_pood_cologne_data(url, website_name, insert_data_func):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    base_url = "https://poodecologne.com/product-range-odor-eliminators-no-bad-smell-stink-free-guarantee-toilet-deodorizer-natural-air-"

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all product sections
    product_sections = soup.find_all("section", class_="wixui-column-strip")

    # Loop through each product section and extract information
    for product in product_sections:
        try:
            # Extract the product name
            product_name_tag = product.find("h2")
            product_name = (
                product_name_tag.get_text(strip=True) if product_name_tag else "N/A"
            )

            # Extract the second <p> tag as description
            description_tags = product.find_all(
                "p", {"class": "font_8 wixui-rich-text__text"}
            )
            product_desc = (
                description_tags[1].get_text(strip=True)
                if len(description_tags) > 1
                else "N/A"
            )

            # Extract image URL and save
            image_tag = product.find("img")
            image_url = (
                image_tag["src"] if image_tag and "src" in image_tag.attrs else None
            )
            image_path = None
            combined_str = product_name + base_url
            hash_value = hashlib.md5(combined_str.encode()).hexdigest()
            product_id = int(hash_value[:8], 16)

            if image_url:
                image_folder = save_images(product_id, website_name, [image_url])
                if not image_folder:
                    print("Image Folder already exists. Skipping !")
                    continue

            # Prepare product data for insertion
            product_data = {
                "website_name": website_name,
                "website_url": url,
                "product_url": base_url,
                "product_id": product_id,
                "product_title": product_name,
                "product_description": product_desc,
                "price": "N/A",
                "vendor": "N/A",
                "product_type": "N/A",
                "tags": "N/A",
                "image_folder": image_folder,
            }

            # Insert product data into the database
            insert_data_func(product_data, image_folder)

            # Print product details for each product
            print(f"Product Name: {product_name}")
            print(f"Description: {product_desc}")
            print(f"Image URL: {image_url}")
            print(f"Image saved at: {image_path}")
            print("-" * 50)

        except Exception as e:
            print(f"An error occurred: {e}")
