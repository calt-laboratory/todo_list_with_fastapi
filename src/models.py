from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    item: str
    completed: bool


class TodoIn(BaseModel):
    item: str
    completed: bool
