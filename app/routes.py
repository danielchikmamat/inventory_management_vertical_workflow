""" api endpoints for inventory management system """

from app.schemas import Item, ItemUpdate, ItemFilter
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import app.service as service
from fastapi import HTTPException, Response
from app.exceptions import ItemNotFoundError, DuplicateItemError, ItemConflictError
from app.db.connection import get_db_connection


router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


@router.post("/items/", status_code=201)
def create_item(item: Item, conn=Depends(get_db_connection)):
    return service.add_item(conn, item)




@router.get("/items/", status_code=200)
def get_items(
    filters: ItemFilter = Depends(), #Depends make it interpret it as query
    conn=Depends(get_db_connection)
    ):

    return service.get_items_filtered(conn, filters)



@router.get("/items/{item_id}")
def fetch_item_by_id(item_id: int, conn=Depends(get_db_connection)):

    return service.get_item_by_id(conn, item_id)



@router.put("/items/{item_id}", status_code=200)
def put_update_item(item_id: int, item_update: ItemUpdate, conn=Depends(get_db_connection)):
    # Implementation for updating an item

    return service.update_item(conn, item_id, item_update)


@router.delete("/items/{item_id}")
def delete_item(item_id: int, conn=Depends(get_db_connection)):
    result = service.delete_item(conn, item_id)
    return result



@router.get("/metrics/stock-value")
def get_stock_value(conn=Depends(get_db_connection)):
    return service.stock_value(conn)