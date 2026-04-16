""" api endpoints for inventory management system """

from src.schemas import Item
from fastapi import APIRouter
from src.service import add_item, view_inventory

router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return add_item(item)


@router.get("/items/")
def get_items():
    # logic to read items from the database
    return view_inventory()
