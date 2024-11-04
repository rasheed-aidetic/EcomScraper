# db/database.py
import sqlite3
import os
import config

# DB_PATH = 'product_data.db'


def initialize_db():
    db_path = config.DB_PATH
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            title TEXT,
            description TEXT,
            price REAL,
            vendor TEXT,
            product_type TEXT,
            tags TEXT,
            image_folder TEXT
        )
        """
        )
        conn.commit()
        conn.close()


def insert_product_data(data, folder_name):
    db_path = config.DB_PATH
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO products (product_id, title, description, price, vendor, product_type, tags, image_folder)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data["id"],
            data.get("title"),
            data.get("body_html"),
            float(data["variants"][0].get("price", 0)),
            data.get("vendor"),
            data.get("product_type"),
            ", ".join(data.get("tags", [])),
            folder_name,
        ),
    )
    conn.commit()
    conn.close()
