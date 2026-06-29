from fastapi import APIRouter,Depends
from pydantic import BaseModel
from core.db import get_db

router = APIRouter()


class Item(BaseModel):
    name:str
    price:int

@router.get("/items")
def get_items(conn=Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(cursor)
    return {"users": users}

@router.post("/items")
def add_items(item:Item):
    return {"message": "Item saved"}