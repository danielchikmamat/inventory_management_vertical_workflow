

from fastapi import FastAPI
from app.db.init_db import init_db
from app.routes import router
from app.handlers import register_exception_handlers
app = FastAPI()

#create table on startup
@app.on_event("startup")
def startup_event():
    init_db()  # Initialize the database when the application starts


#include routes
app.include_router(router)

register_exception_handlers(app)