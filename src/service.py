""" business logic for inventory management system """

from src.repository import delete_item, get_item_by_id, insert_data, fetch_items_filtered

def get_items_filtered(
    threshold: int = None,
    # add more filters here as needed
):
    return fetch_items_filtered(threshold)


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


def remove_item(item_id):
    return delete_item(item_id)

