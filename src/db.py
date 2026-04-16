""" Database operations for inventory management system """
import sqlite3
DB_NAME = 'inventory.db'

def get_db_connection():
    # logic to connect to the database
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn