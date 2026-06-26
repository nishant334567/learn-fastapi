# Routing in FastAPI

## main.py vs routers
- `main.py` is the entry point — creates the app, registers routers
- Don't put all routes in `main.py` — split by resource

## APIRouter
- Like a mini-app for a specific resource
- `main.py` wires them together with `include_router`

```python
# routers/items.py
router = APIRouter()

@router.get("/items")
def get_items():
    return {"items": []}
```

```python
# main.py
from routers import items
app.include_router(items.router)
```

## Folder structure
```
main.py
routers/
  items.py
  users.py
core/
  db.py
```
