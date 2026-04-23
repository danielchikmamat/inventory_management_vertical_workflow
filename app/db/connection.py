""" Database operations for inventory management system """
import sqlite3


def get_db_connection():
    # logic to connect to the database
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()