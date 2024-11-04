# main.py
from config import WEBSITES
from db.database import initialize_db, insert_product_data
from shopify_scraper.scraper import scrape_website
from utils.utils import check_platform
from dotenv import load_dotenv

load_dotenv()


def main():
    initialize_db()
    for website_url in WEBSITES:
        print(f"Checking platform for {website_url}")
        platform = check_platform(website_url)
        website_name = website_url.split("//")[-1].replace("www.", "").split(".")[0]
        if platform == "Shopify":
            print(f"{website_url} is a Shopify site. Starting scraping...")
            try:
                scrape_website(website_url, website_name, insert_product_data)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error scraping {website_url}: {e}")
        else:
            print(
                f"{website_url} is not a supported platform. Detected platform: {platform}"
            )

    print("Data scraping completed.")


if __name__ == "__main__":
    main()
