# inventory_management_vertical_workflow

## vertical workflow
- develop one feature from api -> backend -> database

## file stack error handling
Client → Pydantic → Router → Service → Repository → DB
- pydantic, ensure correct data type
- router, raises http exception (how do we tell the client)
- service, validate logic such as quantity being above 0 (what went wrong)
- repository, try clause where we change the state of the db (INSERT, DELETE, UPDATE) (db errors)