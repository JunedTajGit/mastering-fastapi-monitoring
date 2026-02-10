from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Fastapi-monitoring")
Instrumentator().instrument(app=app).expose(app=app)


class Item(BaseModel):
    id: int
    name: str


items = []


@app.post("/items/create")
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items")
async def get_items():
    return items
