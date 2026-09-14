from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Todo API",
    description="A simple in-memory Todo API built with FastAPI",
    version="1.0.0",
)

# Temporary in-memory dictionary to store todos
# Structure: {todo_id: {"id": int, "title": str, "description": str, "completed": bool}}
todos: dict[int, dict] = {}
id_counter: int = 1


# --- Pydantic Schemas ---
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, and bread")
    completed: bool = Field(default=False)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, bread, and fruits")
    completed: Optional[bool] = Field(None)


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool


# --- API Endpoints ---
@app.get("/")
def root():
    return {
        "message": "Welcome to the FastAPI Todo App!",
        "docs_url": "/docs",
        "total_todos": len(todos),
    }


@app.get("/todos", response_model=List[TodoResponse])
def get_todos(completed: Optional[bool] = None):
    """Retrieve all todo items with an optional completed status filter."""
    todo_list = list(todos.values())
    if completed is not None:
        todo_list = [todo for todo in todo_list if todo["completed"] == completed]
    return todo_list


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """Retrieve a single todo item by its ID."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
    return todos[todo_id]


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """Create a new todo item."""
    global id_counter
    new_todo = {
        "id": id_counter,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }
    todos[id_counter] = new_todo
    id_counter += 1
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update an existing todo item."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    current_todo = todos[todo_id]
    update_data = todo_update.model_dump(exclude_unset=True)

    current_todo.update(update_data)
    todos[todo_id] = current_todo
    return current_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int):
    """Delete a todo item by its ID."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
    deleted_todo = todos.pop(todo_id)
    return {
        "message": f"Todo with ID {todo_id} deleted successfully",
        "deleted_item": deleted_todo,
    }