
from fastapi import APIRouter, Depends, HTTPException

from app.database.fake_db        import FakeDatabase
from app.dependencies.db         import get_db
from app.dependencies.pagination import PaginationParams, get_pagination, paginate_list
from app.dependencies.auth       import verify_token
from app.src.items.model         import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


# ── LIST — pagination + search injected via Depends() ────────
@router.get("/", summary="List all items (paginated)")
def list_items(
    db:     FakeDatabase     = Depends(get_db),
    params: PaginationParams = Depends(get_pagination),
):
    all_items = db.get_all_items()
    return paginate_list(all_items, params)


# ── CREATE ────────────────────────────────────────────────────
@router.post("/", status_code=201, summary="Create a new item")
def create_item(
    body: ItemCreate,
    db:   FakeDatabase = Depends(get_db),
):
    return db.create_item(name=body.name, price=body.price)


# ── GET ONE ───────────────────────────────────────────────────
@router.get("/{item_id}", summary="Get item by ID")
def get_item(
    item_id: int,
    db: FakeDatabase = Depends(get_db),
):
    item = db.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


# ── UPDATE ────────────────────────────────────────────────────
@router.patch("/{item_id}", summary="Update item (partial)")
def update_item(
    item_id: int,
    body:    ItemUpdate,
    db:      FakeDatabase = Depends(get_db),
):
    changes = {k: v for k, v in body.model_dump().items() if v is not None}
    updated = db.update_item(item_id, changes)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return updated


# ── DELETE (protected) ────────────────────────────────────────
@router.delete(
    "/{item_id}",
    summary="Delete item  🔐 requires X-Token header",
    dependencies=[Depends(verify_token)],
)
def delete_item(
    item_id: int,
    db: FakeDatabase = Depends(get_db),
):
    """
    Header required:  X-Token: secret-day3-token
    """
    if not db.delete_item(item_id):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return {"message": f"Item {item_id} deleted successfully"}
