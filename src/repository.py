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


def update_item_by_id(item_id, name=None, quantity=None, price=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    params = []

    if name is not None:
        fields.append("name = ?")
        params.append(name)
    if quantity is not None:
        fields.append("quantity = ?")
        params.append(quantity)
    if price is not None:
        fields.append("price = ?")
        params.append(price)

    if not fields:
        return False  # No fields to update

    params.append(item_id)
    query = f"UPDATE items SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(params))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def calculate_stock_value():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity * price) AS stock_value FROM items")
    result = cursor.fetchone()
    conn.close()

    return result["stock_value"] if result else 0