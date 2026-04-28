""" initialize the database for inventory management system """
import sqlite3

DB_PATH  = "./data/inventory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open("app/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

