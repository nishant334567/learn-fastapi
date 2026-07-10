from fastapi import FastAPI
from routers import agents
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(agents.router)


@app.get("/")
def ping():
    return {"message": "pong"}
