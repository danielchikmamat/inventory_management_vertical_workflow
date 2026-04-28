# inventory_management_vertical_workflow

Inventory management API written with FastAPI and sqlite3.

## Installation

```bash
git clone https://github.com/danielchikmamat/inventory_management_vertical_workflow.git
```

create a virtual enviroment
```bash
python -m venv venv
```

- for Mac/Linux:
```bash
source venv/bin/activate
```
- for Windows:
```bash
venv\Scripts\activate
```
install the dependencies from requirements.txt

```bash
pip install -r requirements.txt
```


## Installation with Docker
```bash
git clone https://github.com/danielchikmamat/inventory_management_vertical_workflow.git
```

From the project root (where the Dockerfile is located):

```bash
docker build -t inventory-management .
```

SQLite stores data in a local file, so create a persistent folder:
```bash
mkdir data

in cmd
```bash
docker run -p 8000:8000 -v %cd%\data:/app/data inventory-management
```
Once running open swagger UI
http://localhost:8000/docs


## Usage

start the FastAPI server
```bash
uvicorn main:app --reload
```
interactive UI use http://127.0.0.1:8000/docs for Swagger UI

start by using the add_item post request to fill your db!

## Tech Stack
- FastAPI (backend framework)
- SQLite3 (database)
- Uvicorn (ASGI server)
- Python

