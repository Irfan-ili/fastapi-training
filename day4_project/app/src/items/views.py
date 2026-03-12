from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List

from database.session  import get_db
from src.items.model   import Item, ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


# ── CREATE ────────────────────────────────────────────────────
@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    body: ItemCreate,
    db: AsyncSession = Depends(get_db),
):

    item = Item(name=body.name, price=body.price)
    db.add(item)
    await db.flush()       # sends INSERT, gets auto-generated id
    await db.refresh(item) # reloads from DB (gets created_at etc.)
    return item


# ── READ ALL ──────────────────────────────────────────────────
@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip:  int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Item).offset(skip).limit(limit)
    )
    return result.scalars().all()


# ── READ ONE ──────────────────────────────────────────────────
@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):

    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


# ── UPDATE ────────────────────────────────────────────────────
@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    body: ItemUpdate,
    db: AsyncSession = Depends(get_db),
):

    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    # Only update fields that were sent in the request
    changes = body.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(item, field, value)

    await db.flush()
    await db.refresh(item)
    return item


# ── DELETE ────────────────────────────────────────────────────
@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):

    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    await db.delete(item)
