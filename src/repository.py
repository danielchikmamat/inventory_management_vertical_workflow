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


def fetch_items_filtered(

        threshold = None,
        # add more filters here as needed
):
    """ default to fetching all items if no filters provided """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM items"
    conditions = []
    params = []

    if threshold is not None:
        conditions.append("quantity < ?")
        params.append(threshold)
    # add more conditions here as needed

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_item_by_id(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    return dict(item) if item else None


def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted