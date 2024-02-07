from fastapi import FastAPI
from models import Todo

app = FastAPI()


todos: list[Todo] = []


@app.get("/todos")
async def get_all_todos() -> dict[str, list[Todo]]:
    return {"todos": todos}


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
