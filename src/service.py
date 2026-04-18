""" business logic for inventory management system """

from src.repository import delete_item, get_item_by_id, insert_data, fetch_items_filtered, calculate_stock_value, update_item_by_id

def get_items_filtered(
    threshold = None,
    min_price = None,
    max_price = None
    # add more filters here as needed
):
    return fetch_items_filtered(threshold, min_price, max_price)


def add_item(item_data):
    item_id = insert_data(item_data.name, item_data.quantity, item_data.price)

    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }


def fetch_item_by_id(item_id):
    return get_item_by_id(item_id)


def update_item(item_id, item_update):
    # Implementation for updating an item
    existing_item = get_item_by_id(item_id)
    if not existing_item:
        return False
    updated = update_item_by_id(item_id, name=item_update.name, quantity=item_update.quantity, price=item_update.price)
    return updated


def remove_item(item_id):
    return delete_item(item_id)


def stock_value():
    total_value = calculate_stock_value()
    return {"total_stock_value": total_value}
