""" business logic for inventory management system """

from src.db import get_db_connection


def add_item(item_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO items (name, quantity, price)
        VALUES (?, ?, ?)
        """,
        (item_data.name, item_data.quantity, item_data.price)
    )

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

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
        return {"error": "Item not found"}

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return {"message": f"Item with id {item_id} has been removed."}