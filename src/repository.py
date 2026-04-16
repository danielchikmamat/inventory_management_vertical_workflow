""" Repository for handling database operations """

from src.db import get_db_connection


def insert_data(name, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO items (name, quantity, price)
        VALUES (?, ?, ?)
        """,
        (name, quantity, price)
    )

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return item_id
