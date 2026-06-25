from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name:str
    price:int

@router.get("/items")
def get_items():
    return {items: []}

@router.post("/items")
def add_items(item:Item):
    return {"message": "Item saved"}