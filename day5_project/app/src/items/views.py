from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.session  import get_db
from src.items.model   import Item, ItemCreate, ItemUpdate, ItemResponse
from src.users.model   import User
from dependencies.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/items", tags=["Items"])
@router.post("/", response_model=ItemResponse, status_code=201,
             summary="Create item  requires login")
async def create_item(
    body:         ItemCreate,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = Item(
        name=body.name,
        price=body.price,
        owner_id=current_user.id,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/", response_model=List[ItemResponse],
            summary="List my items  requires login")
async def list_my_items(
    skip:         int = 0,
    limit:        int = 10,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Item)
        .where(Item.owner_id == current_user.id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/all", response_model=List[ItemResponse],
            summary="List ALL items  admin only")
async def list_all_items(
    skip:  int = 0,
    limit: int = 10,
    db:    AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{item_id}", response_model=ItemResponse,
            summary="Get item  requires login")
async def get_item(
    item_id:      int,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Users can only see their own items; admins can see all
    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your item")
    return item


@router.patch("/{item_id}", response_model=ItemResponse,
              summary="Update item  owner or admin")
async def update_item(
    item_id:      int,
    body:         ItemUpdate,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your item")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204,
               summary="Delete item  owner or admin")
async def delete_item(
    item_id:      int,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your item")
    await db.delete(item)
