""" api endpoints for inventory management system """

from src.schemas import Item
from fastapi import APIRouter
from src.service import add_item, remove_item, view_inventory

router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return add_item(item)


@router.get("/items/")
def get_items():
    return view_inventory()


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    return remove_item(item_id)