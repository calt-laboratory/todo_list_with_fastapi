from fastapi import FastAPI
from models import Todo

app = FastAPI()


todos: list[Todo] = []


# Get all todos
@app.get("/todos")
async def get_todos() -> dict[str, list[Todo]]:
    return {"todos": todos}


# Get a single todo
@app.get("/todos/{todo_id}")
async def get_single_todo(todo_id: int) -> dict[str, Todo | str]:
    for todo in todos:
        if todo.id == todo_id:
            return {"todo": todo}
        return {"message": "Todo not found."}



# Create a new todo
@app.post("/todos")
async def create_todos(todo: Todo) -> dict[str, str]:
    todos.append(todo)
    return {"message": "Todo has been added successfully."}


# Update a todo
