""" business logic for inventory management system """

import app.repo.repository as repo
from app.exceptions import ItemNotFoundError, ItemConflictError


def get_items_filtered(
    conn,
    filters
):
    data = filters.model_dump(exclude_none=True)
    min_price = data.get("min_price")
    max_price = data.get("max_price")

    if min_price is not None and max_price is not None:
        if min_price >= max_price:
            raise ValueError("min price cannot be greater or equal to max price")

    items = repo.get_items_filtered(conn, **data)
    if not items:
        raise ItemNotFoundError("no items found")
    return items


def add_item(conn, item_data):

    item_id = repo.add_data(
        conn,
        item_data.name,
        item_data.quantity,
        item_data.price
    )

    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }


def get_item_by_id(conn, item_id):

    item = repo.get_item_by_id(conn, item_id)
    if item is None:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return item


def update_item(conn, item_id, item_update):
    data = item_update.model_dump(exclude_none=True)

    if not data:
        raise ValueError("No fields provided")

    result = repo.update_item(conn, item_id, **data)

    if result.reason == "not_found":
        raise ItemNotFoundError("Item not found")

    if result.reason == "conflict":
        raise ItemConflictError("Name already exists")

    return result.item



def delete_item(conn, item_id):

    return repo.delete_item(conn, item_id)


def stock_value(conn):

    total_value = repo.stock_value(conn)
    return {"total_stock_value": total_value}

