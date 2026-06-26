# PostgreSQL + psycopg2 in FastAPI

## Libraries
- `psycopg2-binary` — talks to PostgreSQL (like the Node `pg` package)
- `python-dotenv` — reads `.env` file (like `dotenv` in Node)

## Connection string
```
postgresql://username:password@localhost:5432/dbname
```
Goes in `.env`, never hardcoded.

## Connection Pool
- Open N connections at startup, reuse them across requests
- Don't open a new connection on every request — slow and wasteful

```python
# core/db.py
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=os.getenv("DATABASE_URL")
)
```

Pool is a module-level variable — created once, lives for the entire app lifetime.

## get_db — borrow and return
```python
def get_db():
    conn = connection_pool.getconn()   # borrow
    try:
        yield conn                     # hand to route
    finally:
        connection_pool.putconn(conn)  # always return, even if route crashes
```

`yield` pauses the function, gives the connection to the route, then runs `finally` after.

## Depends — dependency injection
FastAPI's way of running `get_db` before the route and injecting the result.

```python
@router.get("/users")
def get_users(conn=Depends(get_db)):
    ...
```

Flow: request → FastAPI runs `get_db` → borrows connection → route runs → connection returned

## Cursor
- Connection = phone call to PostgreSQL
- Cursor = person speaking on the call

```python
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
```

One connection, can have multiple cursors. Always fetch before next execute.


## os.getenv vs Node
```javascript
// Node
process.env.DATABASE_URL
```
```python
# Python
import os
os.getenv("DATABASE_URL")
```

## Prod vs what we did
| | Our setup | Prod |
|---|---|---|
| Driver | psycopg2 (sync) | asyncpg (async) |
| Pool | SimpleConnectionPool | SQLAlchemy / PgBouncer |
| Style | sync routes | async/await routes |

Our setup is fine for learning. Switch to async when deploying.
