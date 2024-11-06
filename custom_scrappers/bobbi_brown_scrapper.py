import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
from utils.utils import save_images


# Function to get all links from a page that end with specified strings
def get_links_ending_with(url, end_string):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if full_url.rstrip("/").endswith(end_string):
                links.append(full_url)
        return list(set(links))
    else:
        print(f"Failed to retrieve {url}")
        return []


# Function to fetch product details from each product link
def fetch_and_save_product_details(
    product_url, website_name, insert_data_func, base_url
):
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        product_title = (
            soup.select_one(".product-full__title").text.strip()
            if soup.select_one(".product-full__title")
            else "N/A"
        )
        price = (
            soup.select_one(".product-full-price__price .price").text.strip()
            if soup.select_one(".product-full-price__price .price")
            else "N/A"
        )

        # Extract detailed description
        product_details_div = soup.find("div", class_="product-full__data-details")
        description = (
            product_details_div.get_text(strip=True, separator=" ")
            if product_details_div
            else "N/A"
        )

        # Extract image URLs
        product_image_div = soup.find("div", class_="product-full__media")
        img_tags = product_image_div.find_all("img") if product_image_div else []
        img_urls = [urljoin(product_url, img.get("src")) for img in img_tags]

        combined_str = product_title + product_url
        hash_value = hashlib.md5(combined_str.encode()).hexdigest()
        unique_id = int(hash_value[:8], 16)

        folder_path = save_images(unique_id, website_name, img_urls)
        if not folder_path:
            print("Image Folder already exists. Skipping !!!!!!!!!!!!!")
        else:

        # Print the extracted information
            print("\nProduct Details:")
            print("Title:", product_title)
            print("Description:", description)
            print("Price:", price)
            print("Image URLs:", img_urls)

            product_data = {
                "website_name": website_name,
                "website_url": base_url,
                "product_url": product_url,
                "product_id": unique_id,
                "product_title": product_title,
                "product_description": description,
                "price": price,
                "vendor": "N/A",
                "product_type": "N/A",
                "tags": "N/A",
                "image_folder": folder_path,
            }

            insert_data_func(product_data, folder_path)
        # print(product_data)

    else:
        print(f"Failed to retrieve product page at {product_url}")


# Main function to get skincare and makeup pages, and then product details
def scrape_product_details(base_url, website_name, insert_data_func):
    # Get skincare and makeup page links
    page_types = ["makeup", "skincare"]
    total_links = []

    for page_type in page_types:
        page_links = get_links_ending_with(base_url, page_type)
        print(page_links)
        if page_links:
            page_url = page_links[0]  # Assuming one main link per page type
            print(f"\n{page_type.capitalize()} page found:", page_url)

            # Scrape the page for product links
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                product_links = []
                product_grid_div = soup.find(
                    "div",
                    class_="field-elc-mpp-content",
                )
                # print(product_grid_div)
                product_links = []

                # Get product links within this specific div
                if product_grid_div:
                    for link in product_grid_div.find_all("a", href=True):
                        full_url = urljoin(page_url, link["href"])
                        # Check if the URL contains "/product/"
                        if "/product/" in full_url:
                            product_links.append(full_url)

                product_links = [url.replace("?vto_open", "") for url in product_links]

                unique_product_links = list(set(product_links))
                total_links.extend(unique_product_links)

                # Print or process each product link and fetch its details
                print("\nProduct Links Found:")

            else:
                print(f"Failed to retrieve {page_type} page at {page_url}")
        else:
            print(f"No {page_type} page link found.")

    total_links = list(set(total_links))
    print(len(total_links))
    for product_link in total_links:  # Limiting to 2 for brevity
        print("Product link:", product_link)
        fetch_and_save_product_details(
            product_link, website_name, insert_data_func, base_url
        )
