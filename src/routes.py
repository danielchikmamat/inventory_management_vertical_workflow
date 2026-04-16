""" api endpoints for inventory management system """

from src.schemas import Item
from fastapi import APIRouter
from src.service import add_item, get_item_by_id, remove_item, view_inventory
from fastapi import HTTPException, Response


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


@router.post("/items/", status_code=201)
def create_item(item: Item):
    return add_item(item)


@router.get("/items/")
def get_items():
    items = view_inventory()
    return items


@router.get("/items/{item_id}")
def fetch_item_by_id(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    success = remove_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)
