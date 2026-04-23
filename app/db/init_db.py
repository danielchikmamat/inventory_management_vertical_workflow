""" initialize the database for inventory management system """
import sqlite3


def init_db(db_path="inventory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open("app/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

