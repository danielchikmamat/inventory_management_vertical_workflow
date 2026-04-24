""" api endpoints for inventory management system """

from app.schemas import Item, ItemUpdate, ItemFilter
from fastapi import APIRouter, Depends
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
    try:
        return service.add_item(conn, item)
    except DuplicateItemError as e:
        raise HTTPException(status_code=409, detail=str(e))



@router.get("/items/", status_code=200)
def get_items(
    filters: ItemFilter = Depends(), #Depends make it interpret it as query
    conn=Depends(get_db_connection)
    ):
    try:
        return service.get_items_filtered(conn, filters)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/items/{item_id}")
def fetch_item_by_id(item_id: int, conn=Depends(get_db_connection)):
    try:
        return service.get_item_by_id(conn, item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/items/{item_id}", status_code=200)
def put_update_item(item_id: int, item_update: ItemUpdate, conn=Depends(get_db_connection)):
    # Implementation for updating an item
    try:
        return service.update_item(conn, item_id, item_update)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ItemConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/items/{item_id}")
def delete_item(item_id: int, conn=Depends(get_db_connection)):
    success = service.delete_item(conn, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)


@router.get("/metrics/stock-value")
def get_stock_value(conn=Depends(get_db_connection)):
    return service.stock_value(conn)