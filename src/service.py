""" business logic for inventory management system """

from src.db import get_db_connection
from src.repository import insert_data

def add_item(item_data):
    item_id = insert_data(item_data.name, item_data.quantity, item_data.price)

    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }

def view_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    if not items:
        return []

    return [dict(item) for item in items]


def get_item_by_id(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    if item:
        return dict(item)
    else:
        return None


def remove_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    item = get_item_by_id(item_id)
    if not item:
        conn.close()
        return None

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()

    conn.close()

    return True