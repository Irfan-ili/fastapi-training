from typing import Optional
from datetime import datetime

# Private storage — never import this directly from routes
_products: dict = {}
_counter: int = 0

def _next_id() -> int:
    global _counter
    _counter += 1
    return _counter

def get_all_products() -> list:
    return list(_products.values())

def get_product(product_id: int) -> Optional[dict]:
    return _products.get(product_id)


def create_product(data: dict) -> dict:
    pid = _next_id()
    data["id"] = pid
    data["created_at"] = datetime.now()
    _products[pid] = data
    return data


def update_product(product_id: int, changes: dict) -> Optional[dict]:
    if product_id not in _products:
        return None
    _products[product_id].update(changes)
    return _products[product_id]


def delete_product(product_id: int) -> bool:
    if product_id not in _products:
        return False
    del _products[product_id]
    return True
