from fastapi import FastAPI
from routers import items, knowledge_base

app = FastAPI()

app.include_router(items.router)
app.include_router(knowledge_base.router)

@app.get("/")
def ping():
    return {"message": "pong"}
