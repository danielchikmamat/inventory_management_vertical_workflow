""" Repository for handling database operations """

from app.db.connection import get_db_connection
import sqlite3 as sqlite3
from app.repo.model import UpdateResult


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


def get_items_filtered(conn, **filters):
    cursor = conn.cursor()

    rules = {
        "threshold": "quantity < ?",
        "min_price": "price >= ?",
        "max_price": "price <= ?",
    }

    conditions = []
    params = []

    try:
        for key, expr in rules.items():
            value = filters.get(key)
            if value is None:
                continue
            conditions.append(expr)
            params.append(value)

        query = "SELECT * FROM items"

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    except sqlite3.Error:
        return []

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