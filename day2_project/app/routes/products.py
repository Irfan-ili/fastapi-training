from fastapi import APIRouter, HTTPException
from typing import List

from app.database.database import (
    get_all_products, get_product,
    create_product, update_product, delete_product
)
from app.models.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create(product: ProductCreate):
    data = product.model_dump()
    return create_product(data)


@router.get("/", response_model=List[ProductResponse])
def read_all():
    return get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
def read_one(product_id: int):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def update(product_id: int, changes: ProductUpdate):
    updates = {k: v for k, v in changes.model_dump().items() if v is not None}
    updated = update_product(product_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}")
def delete(product_id: int):
    if not delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {product_id} deleted"}
