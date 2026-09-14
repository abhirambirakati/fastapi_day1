# FastAPI Day 1 - In-Memory Todo App

A simple FastAPI Todo API storing tasks in a temporary in-memory Python dictionary without requiring a database.

## Features
- **In-memory storage**: Uses a Python dictionary (`todos: dict[int, dict]`) to manage items during runtime.
- **Data validation**: Pydantic models for request bodies and response schemas.
- **CRUD operations**:
  - `GET /todos` - List all todos (supports filtering by `?completed=true|false`)
  - `GET /todos/{todo_id}` - Get a specific todo by ID
  - `POST /todos` - Create a new todo item
  - `PUT /todos/{todo_id}` - Update a todo item (supports partial updates)
  - `DELETE /todos/{todo_id}` - Delete a todo item
- **Interactive Documentation**: Swagger UI at `/docs` and ReDoc at `/redoc`.

---

## Getting Started

### 1. Activate Virtual Environment
```powershell
.\env\Scripts\Activate.ps1
```

### 2. Run the Development Server
```powershell
uvicorn main:app --reload
```

### 3. Access the API & Docs
- **Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
