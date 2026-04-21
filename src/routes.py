""" api endpoints for inventory management system """

from src.schemas import Item, ItemUpdate
from fastapi import APIRouter, Depends
import src.service as service
from fastapi import HTTPException, Response
from src.exceptions import ItemNotFoundError, DuplicateItemError
from src.db.connection import get_db_connection


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


@router.post("/items/", status_code=201)
def create_item(item: Item, conn=Depends(get_db_connection)):
    try:
        return service.add_item(conn, item)
    except DuplicateItemError as e:
        raise HTTPException(status_code=409, detail=str(e))



@router.get("/items/")
def get_items(
    threshold: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    conn=Depends(get_db_connection)
    # add more filters here as needed
    ):
    return service.get_items_filtered(conn, threshold, min_price, max_price)


@router.get("/items/{item_id}")
def fetch_item_by_id(item_id: int, conn=Depends(get_db_connection)):
    try:
        return service.get_item(conn, item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/items/{item_id}")
def put_update_item(item_id: int, item_update: ItemUpdate, conn=Depends(get_db_connection)):
    # Implementation for updating an item
    try:
        return service.update_item(item_id, item_update, conn)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/items/{item_id}")
def delete_item(item_id: int, conn=Depends(get_db_connection)):
    success = service.delete_item(conn, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)


@router.get("/metrics/stock-value")
def get_stock_value(conn=Depends(get_db_connection)):
    return service.stock_value(conn)