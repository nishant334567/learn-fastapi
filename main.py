from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import items, knowledge_base, query
from core.vectorstore import vectorstore

@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = vectorstore  # triggers PGVector init and table creation on startup
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(items.router)
app.include_router(knowledge_base.router)
app.include_router(query.router)

@app.get("/")
def ping():
    return {"message": "pong"}
