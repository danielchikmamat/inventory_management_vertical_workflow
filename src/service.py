""" business logic for inventory management system """

import src.repository as repo
from src.exceptions import ItemNotFoundError, DuplicateItemError
import sqlite3 as sqlite3
from src.db.connection import get_db_connection

def get_items_filtered(
    db = "inventory.db",
    threshold = None,
    min_price = None,
    max_price = None
    # add more filters here as needed
):
    conn = get_db_connection(db)
    return repo.get_items_filtered(conn, threshold, min_price, max_price)


def add_item(item_data, db="invetory.db"):
    conn = get_db_connection(db)
    try:
        item_id = repo.add_data(conn, item_data.name, item_data.quantity, item_data.price)
    except sqlite3.IntegrityError:
        raise DuplicateItemError("item already exists")
    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }


def get_item_by_id(item_id, db="inventory.db"):
    conn = get_db_connection(db)
    item = repo.get_item_by_id(conn, item_id)
    if item is None:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return item


def update_item(item_id, item_update, db="inventory.db"):
    # Implementation for updating an item
    conn = get_db_connection(db)
    get_item_by_id(conn, item_id) #ensures items exist, raises exception
    if repo.item_name_exists(conn, item_update.name):
        raise DuplicateItemError(f"Name {item_update.name} already exists ")

    updated = repo.update_item(
        conn,
        item_id,
        name=item_update.name,
        quantity=item_update.quantity,
        price=item_update.price)
    return updated


def delete_item(item_id, db="inventory.db"):
    conn = get_db_connection(db)
    return repo.delete_item(conn, item_id)


def stock_value(db="inventory.db"):
    conn = get_db_connection(db)
    total_value = repo.stock_value(conn)
    return {"total_stock_value": total_value}

