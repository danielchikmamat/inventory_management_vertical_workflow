""" api endpoints for inventory management system """

from src.schemas import Item
from fastapi import APIRouter
from src.service import add_item

router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return add_item(item)