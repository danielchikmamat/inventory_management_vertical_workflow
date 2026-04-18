""" business logic for inventory management system """

import src.repository as repo
from src.exceptions import ItemNotFoundError, DuplicateItemError
import sqlite3 as sqlite3

def get_items_filtered(
    threshold = None,
    min_price = None,
    max_price = None
    # add more filters here as needed
):
    return repo.get_items_filtered(threshold, min_price, max_price)


def add_item(item_data):
    try:
        item_id = repo.add_data(item_data.name, item_data.quantity, item_data.price)
    except sqlite3.IntegrityError:
        raise DuplicateItemError("item already exists")
    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }


def get_item_by_id(item_id):
    item = repo.get_item_by_id(item_id)
    if item is None:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return item


def update_item(item_id, item_update):
    # Implementation for updating an item

    get_item_by_id(item_id) #ensures items exist, raises exception
    if repo.item_name_exists(item_update.name):
        raise DuplicateItemError(f"Name {update_item.name} already exists ")

    updated = repo.update_item(item_id,
        name=item_update.name,
        quantity=item_update.quantity,
        price=item_update.price)
    return updated


def delete_item(item_id):
    return repo.delete_item(item_id)


def stock_value():
    total_value = repo.stock_value()
    return {"total_stock_value": total_value}

