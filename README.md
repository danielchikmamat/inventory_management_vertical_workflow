# inventory_management_vertical_workflow

## vertical workflow
- develop one feature from api -> backend -> database

## file stack error handling
Client → Pydantic → Router → Service → Repository → DB
- pydantic, ensure correct data type
- router, raises http exception (how do we tell the client)
- service, validate logic such as quantity being above 0 (what went wrong)
- repository, try clause where we change the state of the db (INSERT, DELETE, UPDATE) (db errors)


## query parameters
- do this /items/ filters (threshold, min_price, max_price) and /items/{item_id} resource id
- instead of /items/low-stock, /item/min-price etc can conflict with router pathing

## sql queries
- never do this cursor.execute("f"SELECT * FROM items WHERE name = '{name}") SQL injection prone
- do this cursor.execute("SELECT * FROM items WHERE name = ?", (name,)). name will be treated as data and not parsed as sql code

## Standardize error
- status code 404 -> not found
- 409 -> duplicate
- 422 -> validation (pydantic)
- return [] or 404?
- what does update return?
- do deletes return body or just status. Returns status code 204

## clean architecture pass
- router -> no SQL
- service -> no SQL
- repository -> no HTTP logic
- DB layer -> only connection handling
