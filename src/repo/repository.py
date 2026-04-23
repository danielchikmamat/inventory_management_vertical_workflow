""" Repository for handling database operations """

from src.db.connection import get_db_connection
import sqlite3 as sqlite3
from src.repo.model import UpdateResult


def add_data(conn, name, quantity, price, ):

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
    return item_id



def get_items_filtered(
        conn,
        threshold = None,
        min_price = None,
        max_price = None
        # add more filters here as needed
):
    """ default to fetching all items if no filters provided """

    cursor = conn.cursor()

    query = "SELECT * FROM items"
    conditions = []
    params = []

    if threshold is not None:
        conditions.append("quantity < ?")
        params.append(threshold)

    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)

    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)
    # add more conditions here as needed

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()


    return [dict(row) for row in rows]


def get_item_by_id(conn, item_id):

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()

    return dict(item) if item else None


def update_item(conn, item_id, **fields) -> UpdateResult:
    cursor = conn.cursor()

    try:
        set_clause = ", ".join(f"{k} = ?" for k in fields)

        cursor.execute(
            f"UPDATE items SET {set_clause} WHERE id = ?",
            list(fields.values()) + [item_id]
        )

        if cursor.rowcount == 0:
            return UpdateResult(0, None, reason="not_found")

        conn.commit()

        row = conn.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()

        return UpdateResult(1, dict(row), reason="ok")

    except sqlite3.IntegrityError:
        # UNIQUE constraint violation → duplicate name
        return UpdateResult(0, None, reason="conflict")


def delete_item(conn, item_id):

    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    deleted = cursor.rowcount > 0
    conn.commit()

    return deleted


def stock_value(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity * price) AS stock_value FROM items")
    result = cursor.fetchone()


    return result["stock_value"] if result else 0


def item_name_exists(conn, name: str) -> bool:

    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM items WHERE name = ? LIMIT 1",
        (name,)
    )

    exists = cursor.fetchone() is not None
    return exists