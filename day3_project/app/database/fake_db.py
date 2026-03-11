
from datetime import datetime
from typing import Optional

# Private in-memory tables (simulate DB tables)
_items_table:    dict = {}
_products_table: dict = {}
_users_table:    dict = {}
_counters:       dict = {"items": 0, "products": 0, "users": 0}


class FakeDatabase:
    """
    TOPIC: Fake DB Dependency + Request-Scoped Session

    A new instance is created per request via Depends(get_db).
    Simulates open / commit / rollback / close like a real DB session.
    """

    def __init__(self):
        self._items    = _items_table
        self._products = _products_table
        self._users    = _users_table

    # ── Session lifecycle ─────────────────────────────────

    def begin(self):
        pass  # simulate open transaction

    def close(self):
        pass  # simulate close session

    # ── Items ─────────────────────────────────────────────

    def get_all_items(self) -> list:
        return list(self._items.values())

    def get_item(self, item_id: int) -> Optional[dict]:
        return self._items.get(item_id)

    def create_item(self, name: str, price: float) -> dict:
        _counters["items"] += 1
        item = {
            "id":         _counters["items"],
            "name":       name,
            "price":      price,
            "created_at": datetime.now().isoformat(),
        }
        self._items[item["id"]] = item
        return item

    def update_item(self, item_id: int, data: dict) -> Optional[dict]:
        if item_id not in self._items:
            return None
        self._items[item_id].update(data)
        return self._items[item_id]

    def delete_item(self, item_id: int) -> bool:
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True

    # ── Products ──────────────────────────────────────────

    def get_all_products(self) -> list:
        return list(self._products.values())

    def get_product(self, product_id: int) -> Optional[dict]:
        return self._products.get(product_id)

    def create_product(self, data: dict) -> dict:
        _counters["products"] += 1
        data["id"]         = _counters["products"]
        data["created_at"] = datetime.now().isoformat()
        self._products[data["id"]] = data
        return data

    def update_product(self, product_id: int, changes: dict) -> Optional[dict]:
        if product_id not in self._products:
            return None
        self._products[product_id].update(changes)
        return self._products[product_id]

    def delete_product(self, product_id: int) -> bool:
        if product_id not in self._products:
            return False
        del self._products[product_id]
        return True

    # ── Users ─────────────────────────────────────────────

    def get_all_users(self) -> list:
        return list(self._users.values())

    def get_user(self, user_id: int) -> Optional[dict]:
        return self._users.get(user_id)

    def create_user(self, username: str, email: str) -> dict:
        _counters["users"] += 1
        user = {
            "id":         _counters["users"],
            "username":   username,
            "email":      email,
            "created_at": datetime.now().isoformat(),
        }
        self._users[user["id"]] = user
        return user
