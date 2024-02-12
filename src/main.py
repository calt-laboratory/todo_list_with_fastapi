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
@app.get("/todos", response_model=list[Todo])
async def get_all_todos() -> list[Record]:
    query = todo_table_schema.select()
    return await database.fetch_all(query)


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_single_todo(todo_id: int) -> Record | None:
    query = f"SELECT * FROM todos WHERE id = {todo_id}"
    return await database.fetch_one(query)


@app.post("/todos", response_model=Todo)
async def create_single_todo(todo: TodoIn) -> dict[str, str]:
    query = todo_table_schema.insert().values(item=todo.item, completed=todo.completed)
    last_record_id = await database.execute(query)
    return {**todo.dict(), "id": last_record_id}


@app.put("/todos/{todo_id}")
async def update_single_todo(todo_id: int, todo_item: Todo) -> dict[str, Todo | str]:
    for todo in todo_table_schema:
        if todo.id == todo_id:
            todo.id = todo_id
            todo.item = todo_item.item
            return {"todo": todo}
    return {"message": "No todo found to update."}


@app.delete("/todos/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict[str, str]:
    for todo in todo_table_schema:
        if todo.id == todo_id:
            todo_table_schema.remove(todo)
            return {"message": "Todo has been removed successfully."}
    return {"message": "Todo not found."}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
