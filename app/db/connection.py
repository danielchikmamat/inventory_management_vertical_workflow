""" Database operations for inventory management system """
import sqlite3

DB_PATH = "./data/inventory.db"

def get_db_connection():
    # logic to connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()