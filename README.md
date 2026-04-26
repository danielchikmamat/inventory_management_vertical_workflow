# inventory_management_vertical_workflow

Inventory management API written with FastAPI and sqlite3.

## Installation

´´´bash
git clone https://github.com/danielchikmamat/inventory_management_vertical_workflow.git
´´´
create a virtual enviroment python -m venv venv

- for Mac/Linux: source venv/bin/activate
- for Windows: venv\Scripts\activate

pip install -r requirements.txt

## Usage

start the FastAPI server
´´´bash
uvicorn main:app --reload
´´´
interactive UI use http://127.0.0.1:8000/docs for Swagger UI

start by using the add_item post request to fill your db!

## Tech Stack
- FastAPI (backend framework)
- SQLite3 (database)
- Uvicorn (ASGI server)
- Python

