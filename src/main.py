import uvicorn
from database import database, engine, metadata, todo_table_schema
from databases.interfaces import Record
from fastapi import FastAPI, HTTPException
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
    """
    Get all todos from the database.
    :return: List of todos
    """
    query = todo_table_schema.select()
    return await database.fetch_all(query)


@app.get(path="/todos/{todo_id}", response_model=Todo)
async def get_single_todo_by_id(todo_id: int) -> Record | None:
    """
    Get a single to-do by id from the database.
    :param todo_id: The id of the to-do to retrieve
    :return: to-do with the specified id
    """
    query = f"SELECT * FROM todos WHERE id = {todo_id}"
    todo = await database.fetch_one(query)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo


@app.post(path="/todos", response_model=Todo)
async def create_single_todo(to_do: TodoIn) -> dict[str, str]:
    """
    Create a single to-do in the database.
    :param to_do: to-do item to create
    :return: Created to-do item
    """
    query = todo_table_schema.insert().values(item=to_do.item, completed=to_do.completed)
    last_record_id = await database.execute(query)
    return {**to_do.dict(), "id": last_record_id}


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_single_todo(todo_id: int, todo_item: TodoIn) -> Record | None:
    """
    Updates a single to-do in the database.
    :param todo_id: id of the to-do item to update
    :param todo_item: Updated to-do item
    :return: Updated to-do item
    """
    query = f"UPDATE todos SET item = '{todo_item.item}', completed = {todo_item.completed} WHERE id = {todo_id}"
    await database.execute(query)
    new_query = f"SELECT * FROM todos WHERE id = {todo_id}"
    return await database.fetch_one(new_query)


@app.delete(path="/todos/{todo_id}", response_model=list[Todo])
async def delete_single_todo(todo_id: int) -> list[Record]:
    """
    Deletes a single to-do from the database.
    :param todo_id: id of the to-do item to delete
    :return: List of remaining to-do items
    """
    query = f"DELETE FROM todos WHERE id = {todo_id}"
    await database.execute(query)
    new_query = todo_table_schema.select()
    return await database.fetch_all(new_query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
