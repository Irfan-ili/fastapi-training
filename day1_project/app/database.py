# This file simulates database behavior using an in-memory list

from app.models import items

def get_all_items():
    return items

def add_item(item):
    items.append(item)
    return item

def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None

def delete_item(item):
    items.remove(item)