from fastapi import APIRouter
from app.database import get_all_items, add_item, find_item, delete_item

router = APIRouter()

# CREATE
@router.post("/items")
def create_item(name: str, price: float):
    items = get_all_items()
    item = {
        "id": len(items) + 1,
        "name": name,
        "price": price
    }
    return add_item(item)

# READ ALL
@router.get("/items")
def get_items():
    return get_all_items()

# READ ONE
@router.get("/items/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)
    if item:
        return item
    return {"message": "Item not found"}

# UPDATE
@router.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    item = find_item(item_id)
    if item:
        item["name"] = name
        item["price"] = price
        return item
    return {"message": "Item not found"}

# DELETE
@router.delete("/items/{item_id}")
def remove_item(item_id: int):
    item = find_item(item_id)
    if item:
        delete_item(item)
        return {"message": "Item deleted"}
    return {"message": "Item not found"}