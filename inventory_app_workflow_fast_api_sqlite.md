# Inventory Management App Workflow

This document outlines a simple, feature-based workflow for building an inventory management system using:
- Python
- FastAPI
- SQLite (raw SQL, no ORM)

---

## 🧩 Overall Flow

```
Client (JSON request)
    ↓
API Endpoint (FastAPI)
    ↓
Backend Logic (Service / Function)
    ↓
Database Layer (Raw SQL)
    ↓
SQLite Database
```

---

## 1. 📥 JSON Request (Client → API)

The client sends data in JSON format.

Example: Add Item

```json
{
  "name": "Keyboard",
  "quantity": 10,
  "price": 50
}
```

---

## 2. 🌐 API Layer (FastAPI)

Defines the endpoint and validates incoming data.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)

@app.post("/items")
def create_item(item: ItemCreate):
    return add_item(item)
```

Responsibilities:
- Receive request
- Validate input (Pydantic)
- Call backend logic

---

## 3. 🧠 Backend Logic (Service Layer)

Handles business rules and database interaction using raw SQL.

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn


def add_item(item_data):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO items (name, quantity, price)
        VALUES (?, ?, ?)
        """,
        (item_data.name, item_data.quantity, item_data.price)
    )

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return {
        "id": item_id,
        "name": item_data.name,
        "quantity": item_data.quantity,
        "price": item_data.price
    }
```

Responsibilities:
- Apply business logic
- Execute SQL queries
- Manage database connection manually

---

## 4. 🗄️ Database Layer (Raw SQLite SQL)

Instead of an ORM, we define tables manually and interact using SQL.

### Table schema

```sql
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
```

Responsibilities:
- Store raw data
- Execute SQL queries via Python

---

## 5. 💾 Database (SQLite)

Stores the actual data on disk in a `.db` file.

Example table structure:

```
items
------
id | name | quantity | price
```

---

## 🔁 End-to-End Flow Example

1. Client sends POST /items with JSON
2. FastAPI endpoint receives request
3. Pydantic validates data
4. `add_item()` is called
5. Raw SQL inserts data into SQLite
6. Database returns inserted row ID
7. Backend returns created item as JSON response

---

## 🧠 Key Principles

- Build one feature end-to-end (vertical slice)
- Keep layers separate (API, logic, database)
- Validate input early using Pydantic
- Use raw SQL carefully and consistently
- Always manage DB connections properly

---

## 🚀 Next Features to Implement

- Get all items (`GET /items`)
- Get single item (`GET /items/{id}`)
- Update item (`PUT /items/{id}`)
- Delete item (`DELETE /items/{id}`)

---

## 📌 Summary

- JSON = input/output format
- FastAPI = API layer
- Backend = business logic
- Raw SQL (sqlite3) = database interaction
- SQLite = data storage

Build each feature by connecting all layers from request → database → response.

