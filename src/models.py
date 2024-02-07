from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    item: str


class TodoIn(BaseModel):
    item: str
    completed: bool
