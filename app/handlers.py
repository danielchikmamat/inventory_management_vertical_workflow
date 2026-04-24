from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.exceptions import (
    ItemNotFoundError,
    DuplicateItemError,
    ItemConflictError,
    DbError,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ItemNotFoundError)
    def item_not_found_handler(request: Request, exc: ItemNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    @app.exception_handler(DuplicateItemError)
    def duplicate_item_handler(request: Request, exc: DuplicateItemError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ItemConflictError)
    def item_conflict_handler(request: Request, exc: ItemConflictError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )

    @app.exception_handler(DbError)
    def db_error_handler(request: Request, exc: DbError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error"}
        )