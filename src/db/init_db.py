""" initialize the database for inventory management system """
import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    with open("src/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

