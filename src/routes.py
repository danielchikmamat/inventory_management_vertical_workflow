""" api endpoints for inventory management system """

from src.schemas import Item, ItemUpdate
from fastapi import APIRouter
from src.service import add_item, get_item_by_id, get_items_filtered, remove_item, stock_value, update_item
from fastapi import HTTPException, Response


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


@router.post("/items/", status_code=201)
def create_item(item: Item):
    return add_item(item)


@router.get("/items/")
def get_items(
    threshold: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    # add more filters here as needed
    ):
    return get_items_filtered(threshold, min_price, max_price)


@router.get("/items/metrics/stock-value")
def get_stock_value():
    return stock_value()


@router.get("/items/{item_id}")
def fetch_item_by_id(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}")
def put_update_item(item_id: int, item_update: ItemUpdate):
    # Implementation for updating an item
    return update_item(item_id, item_update)


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    success = remove_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)


