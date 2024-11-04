import os
import sqlite3
import json
from dotenv import load_dotenv



def initialize_database(db_path):
    # Check if the database already exists
    if not os.path.exists(db_path):
        print("Creating database...")
        # Connect to SQLite (this will create the db if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the ProductDetail table
        create_table_query = """
        CREATE TABLE ProductDetail (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            description TEXT,
            title TEXT,
            image_paths JSON,
            price REAL,
            url TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Database and ProductDetail table created successfully.")
    else:
        print("Database already exists.")


