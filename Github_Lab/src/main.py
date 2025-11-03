from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory storage
items: Dict[int, dict] = {}
next_id = 1


class Item(BaseModel):
    name: str
    description: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items")
def create_item(item: Item):
    global next_id
    item_id = next_id
    items[item_id] = {"id": item_id, **item.dict()}
    next_id += 1
    return items[item_id]


@app.get("/items")
def read_items():
    return list(items.values())


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = {"id": item_id, **item.dict()}
    return items[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}