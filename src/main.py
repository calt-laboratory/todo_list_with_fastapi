import uvicorn
from database import database, engine, metadata, todo_table_schema
from databases.interfaces import Record
from fastapi import FastAPI
from models import Todo, TodoIn

metadata.create_all(engine)

app = FastAPI()


# Lifecycle events
@app.on_event("startup")
async def startup() -> None:
    """Connect to the database when the application starts."""
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown the database connection when the application stops."""
    await database.disconnect()


# Routes
@app.get(path="/todos", response_model=list[Todo])
async def get_all_todos() -> list[Record]:
    query = todo_table_schema.select()
    return await database.fetch_all(query)


@app.get(path="/todos/{todo_id}", response_model=Todo)
async def get_single_todo(todo_id: int) -> Record | None:
    query = f"SELECT * FROM todos WHERE id = {todo_id}"
    return await database.fetch_one(query)


@app.post(path="/todos", response_model=Todo)
async def create_single_todo(todo: TodoIn) -> dict[str, str]:
    query = todo_table_schema.insert().values(item=todo.item, completed=todo.completed)
    last_record_id = await database.execute(query)
    return {**todo.dict(), "id": last_record_id}


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_single_todo(todo_id: int, todo_item: TodoIn) -> Record | None:
    query = f"UPDATE todos SET item = '{todo_item.item}', completed = {todo_item.completed} WHERE id = {todo_id}"
    await database.execute(query)
    new_query = f"SELECT * FROM todos WHERE id = {todo_id}"
    return await database.fetch_one(new_query)


@app.delete(path="/todos/{todo_id}", response_model=list[Todo])
async def delete_single_todo(todo_id: int) -> list[Record]:
    query = f"DELETE FROM todos WHERE id = {todo_id}"
    await database.execute(query)
    new_query = todo_table_schema.select()
    return await database.fetch_all(new_query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
