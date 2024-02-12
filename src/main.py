import uvicorn
from database import database, engine, metadata, todos
from databases.interfaces import Record
from fastapi import FastAPI
from models import Todo

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
    query = todos.select()
    return await database.fetch_all(query)


@app.get("/todos/{todo_id}")
async def get_single_todo(todo_id: int) -> dict[str, Todo | str]:
    for todo in todos:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": "Todo not found."}


@app.post("/todos")
async def create_single_todo(todo: Todo) -> dict[str, str]:
    todos.append(todo)
    return {"message": "Todo has been added successfully."}


@app.put("/todos/{todo_id}")
async def update_single_todo(todo_id: int, todo_item: Todo) -> dict[str, Todo | str]:
    for todo in todos:
        if todo.id == todo_id:
            todo.id = todo_id
            todo.item = todo_item.item
            return {"todo": todo}
    return {"message": "No todo found to update."}


@app.delete("/todos/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict[str, str]:
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo has been removed successfully."}
    return {"message": "Todo not found."}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
