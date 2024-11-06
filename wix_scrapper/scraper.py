# shopify_scraper/scraper.py
import requests
from utils.utils import save_images
import re, json
import hashlib
from bs4 import BeautifulSoup



def fetch_product_data_for_luvottica(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main menu and extract category and subcategory links
    categories = []

    # Loop through each top-level category
    categories_to_skip = ["HOME", "Contact Us", "Collaborate", "Blog", "Download"]
    for item in soup.select('.StylableHorizontalMenu3372578893__menu > .itemDepth02233374943__itemWrapper'):
        category_name = item.select_one('.itemDepth02233374943__label').text.strip()
        if category_name in categories_to_skip:
            continue
        category_link = item.select_one('a')['href']
        category_info = {'name': category_name, 'link': category_link}

        categories.append(category_info)
    
    # Step 2: Get all products from each category with pagination
    all_products = []
    for category in categories:
        page = 1
        while True:
            category_url = f"{category['link']}?page={page}"
            response = requests.get(category_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Loop through each product item in the list
            products = soup.select('li[data-hook="product-list-grid-item"]')
            print(category["name"], page, len(products))
            if len(products) == 0:
                break
            for item in products:
                # Get the title
                title = item.select_one('p[data-hook="product-item-name"]').text.strip()
                # Get the link
                link = item.select_one('a[data-hook="product-item-container"]')['href']
                
                # Append to list
                all_products.append({
                    'category' : category["name"],
                    'title': title,
                    'link': link
                })

                    
            page += 1

    return all_products

def scrap_and_extract_images_from_luvottica(product):
    url = product["link"]
    response = requests.get(url)
    import time
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the product title
    title = soup.select_one('h1[data-hook="product-title"]').text.strip()

    # Generate a unique hash for the product and convert it to an integer
    combined_str = title + url
    hash_value = hashlib.md5(combined_str.encode()).hexdigest()
    unique_id = int(hash_value[:8], 16)  # Convert the first 8 characters of the hash to an integer

    
    # Extract the product description
    description = soup.select_one('pre[data-hook="description"]').text.strip()
    price = soup.select_one('span[data-hook="formatted-primary-price"]').text.strip()
    
    # Extract features (assuming they are in a list under a specific class)
    features = [feature.text.strip() for feature in soup.select('div[data-hook="info-section-description"] ul li')]
    
    
    # Extract high-resolution image links from thumbnails
    all_images = []
    for thumb in soup.select('div[data-hook="thumbnails"] img'):
        # Replace thumbnail dimensions to get high-resolution versions if needed
        high_res_url = thumb['src'].replace('/w_45,h_45', '/w_500,h_500')  # or other size
        all_images.append(high_res_url)
    
    
    product_data = {
        "id" : unique_id,
        "title" : title,
        "description" : description,
        "features" : features,
        "price" : price,
        "images" : all_images
    }
    
    return product_data
        

from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_website(url, website_name, insert_data_func):
    products = fetch_product_data_for_luvottica(url)
    print(f"{website_name} : {len(products)}")

    def process_product(product):
        if product["title"] == "Men's Red and Royal Blue Microfiber Free Size Thong Underwear":
            return
        print(f"Fetching product data for {website_name} : {product.get('link')}")
        extracted_product_data = scrap_and_extract_images_from_luvottica(product)
        image_folder = save_images(extracted_product_data["id"], website_name, extracted_product_data.get("images"))
        if not image_folder:
            print("Image Folder already exists. Skipping !!!!!!!!!!!!!")
            return
        
        # Clean the price string to remove currency symbols and other non-numeric characters
        price_str = extracted_product_data.get("price", "")
        cleaned_price = re.sub(r'[^\d.]', '', price_str)  # Removes non-numeric characters except decimal points
        
        try:
            price = float(cleaned_price)
        except ValueError:
            print(f"Error: Invalid price format for product {product.get('link')}: {price_str}")
            return
        product_data = {
            "website_name" : website_name,
            "website_url" : url,
            "product_url" : product.get("link"),
            "product_id" : extracted_product_data.get("id"),
            "product_title" : extracted_product_data.get("title"),
            "product_description" : extracted_product_data.get("description"),
            "price" : price,
            "vendor" : website_name,
            "product_type" : extracted_product_data.get("product_type", ""),
            "tags" : ", ".join(extracted_product_data.get("features", [])),
            "image_folder" : image_folder
        }

        print(product_data, "\n\n\n")
        
        insert_data_func(product_data, image_folder)

    # Use ThreadPoolExecutor for threading in the for loop
    with ThreadPoolExecutor(max_workers=5) as executor:  # Set max_workers as needed
        futures = [executor.submit(process_product, product) for product in products]
        
        for future in as_completed(futures):
            future.result()  # This ensures any exceptions are raised