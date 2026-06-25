# Learning FastAPI

A hands-on project where I learn FastAPI by building an agentic RAG (Retrieval-Augmented Generation) API step by step.

## Progress

- [x] Basic FastAPI app with a health check route
- [x] Pydantic models for request validation
- [x] APIRouter — splitting routes across multiple files

## Project Structure

```
agentic-rag-fastapi/
├── main.py          # App entry point, root route
├── routers/
│   └── items.py     # Items routes (GET, POST /items)
└── README.md
```

## Run Locally

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn

# Start the server
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`

## API Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Health check |
| GET | `/items` | List items |
| POST | `/items` | Create an item |

Interactive docs available at `http://127.0.0.1:8000/docs`
