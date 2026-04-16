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