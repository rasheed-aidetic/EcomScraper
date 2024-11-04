from dotenv import load_dotenv
from db_utils.utils import initialize_database
import os

load_dotenv()
# Get the root directory where main.py is located
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "database.sqlite3")


if __name__ == "__main__":
    initialize_database(DB_PATH)
