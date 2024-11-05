# main.py
from config import WEBSITES
from db.database import initialize_db, insert_product_data
from shopify_scraper.scraper import scrape_website
from utils.utils import check_platform
from dotenv import load_dotenv
import concurrent.futures
import traceback

load_dotenv()




def main():
    initialize_db()

    def process_website(website_url):
        website_url = website_url.rstrip('/')
        print(f"Checking platform for {website_url}")
        
        platform = check_platform(website_url)
        website_name = website_url.split("//")[-1].replace("www.", "").split(".")[0]
        
        if platform == "Shopify":
            print(f"{website_url} is a Shopify site. Starting scraping...")
            try:
                scrape_website(website_url, website_name, insert_product_data)
            except Exception as e:
                traceback.print_exc()
                print(f"Error scraping {website_url}: {e}")
        else:
            print(f"{website_url} is not a supported platform. Detected platform: {platform}")

    # Use ThreadPoolExecutor to process each website in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_website, WEBSITES)

    print("Data scraping completed.")

if __name__ == "__main__":
    main()
