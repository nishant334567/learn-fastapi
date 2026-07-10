from fastapi import FastAPI
from routers import agents

app = FastAPI()

app.include_router(agents.router)


@app.get("/")
def ping():
    return {"message": "pong"}
