
from fastapi import APIRouter, Depends, HTTPException

from app.database.fake_db        import FakeDatabase
from app.dependencies.db         import get_db
from app.dependencies.pagination import PaginationParams, get_pagination, paginate_list
from app.dependencies.auth       import verify_token
from app.src.products.model      import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", summary="List all products (paginated)")
def list_products(
    db:     FakeDatabase     = Depends(get_db),
    params: PaginationParams = Depends(get_pagination),  # ← same as items!
):
    return paginate_list(db.get_all_products(), params)


@router.post("/", status_code=201, summary="Create a new product")
def create_product(
    body: ProductCreate,
    db:   FakeDatabase = Depends(get_db),
):
    return db.create_product(body.model_dump())


@router.get("/{product_id}", summary="Get product by ID")
def get_product(
    product_id: int,
    db: FakeDatabase = Depends(get_db),
):
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@router.patch("/{product_id}", summary="Update product (partial)")
def update_product(
    product_id: int,
    body: ProductUpdate,
    db:   FakeDatabase = Depends(get_db),
):
    changes = {k: v for k, v in body.model_dump().items() if v is not None}
    updated = db.update_product(product_id, changes)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return updated


@router.delete(
    "/{product_id}",
    summary="Delete product  🔐 requires X-Token header",
    dependencies=[Depends(verify_token)],
)
def delete_product(
    product_id: int,
    db: FakeDatabase = Depends(get_db),
):
    if not db.delete_product(product_id):
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return {"message": f"Product {product_id} deleted successfully"}
