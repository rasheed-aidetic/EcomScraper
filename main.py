# main.py
from config import WEBSITES
from db.database import initialize_db, insert_product_data
from shopify_scraper.scraper import scrape_website
from utils.utils import check_platform
from dotenv import load_dotenv

load_dotenv()


def main():
    initialize_db()
    for website in WEBSITES:
        print(f"Checking platform for {website}")
        platform = check_platform(website)

        if platform == "Shopify":
            print(f"{website} is a Shopify site. Starting scraping...")
            try:
                scrape_website(website, insert_product_data)
            except Exception as e:
                print(f"Error scraping {website}: {e}")
        else:
            print(
                f"{website} is not a supported platform. Detected platform: {platform}"
            )

    print("Data scraping completed.")


if __name__ == "__main__":
    main()
