

from fastapi import FastAPI
from src.init_db import init_db
from src.routes import router

app = FastAPI()

#create table on startup
@app.on_event("startup")
def startup_event():
    init_db()  # Initialize the database when the application starts


#include routes
app.include_router(router)

