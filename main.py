# main.py
from dotenv import load_dotenv

load_dotenv()
from config import WEBSITES
from db.database import initialize_db, insert_product_data
from shopify_scraper.scraper import scrape_website as scrape_shopify_website
from woocommerce_scrapper.scraper import scrape_website as scrape_woocommerce_website
from custom_scrappers.scraper import scrape_pood_cologne_data
from utils.utils import check_platform
from custom_scrappers.bobbi_brown_scrapper import scrape_product_details as bobbi_brown_scrapper

import concurrent.futures
import traceback


def main():
    initialize_db()

    def process_website(website_url):
        website_url = website_url.rstrip("/")
        print(f"Checking platform for {website_url}")

        platform = check_platform(website_url)
        website_name = website_url.split("//")[-1].replace("www.", "").split(".")[0]

        if platform == "Shopify":
            print(f"{website_url} is a Shopify site. Starting scraping...")
            try:
                scrape_shopify_website(website_url, website_name, insert_product_data)
                print(f"Scraping completed for {website_url}")
            except Exception as e:
                traceback.print_exc()
                print(f"Error scraping {website_url}: {e}")

        elif website_url == "https://www.bobbibrown.in":
            bobbi_brown_scrapper(website_url, website_name, insert_product_data)

        elif website_url == "https://poodecologne.com":
            scrape_pood_cologne_data(website_url, website_name, insert_product_data)

        elif platform == "Woocommerce":
            print(f"{website_url} is a woocommerce site. Starting scraping...")
            try:
                scrape_woocommerce_website(
                    website_url, website_name, insert_product_data
                )
                print(f"Scraping completed for {website_url}")
            except Exception as e:
                traceback.print_exc()
                print(f"Error scraping {website_url}: {e}")
        else:
            print(
                f"{website_url} is not a supported platform. Detected platform: {platform}"
            )

    # Use ThreadPoolExecutor to process each website in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_website, WEBSITES)

    print("Data scraping completed.")


if __name__ == "__main__":
    main()
