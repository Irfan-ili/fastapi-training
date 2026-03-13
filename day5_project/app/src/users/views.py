from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.session   import get_db
from src.users.model    import User, UserResponse, UserUpdate
from dependencies.auth  import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])


# ── List all users — Admin only ───────────────────────────────
@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users admin only",
)
async def list_users(
    skip:  int = 0,
    limit: int = 10,
    db:    AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),  # ← admin only
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# ── Get any user by ID — Admin only ──────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID admin only",
)
async def get_user(
    user_id: int,
    db:      AsyncSession = Depends(get_db),
    admin:   User = Depends(get_current_admin),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


# ── Update own profile — Logged in ───────────────────────────
@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update my profile requires login",
)
async def update_me(
    body:         UserUpdate,
    db:           AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ← any logged-in user
):
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    await db.flush()
    await db.refresh(current_user)
    return current_user


# ── Deactivate user — Admin only ──────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Deactivate user admin only",
)
async def deactivate_user(
    user_id: int,
    db:      AsyncSession = Depends(get_db),
    admin:   User = Depends(get_current_admin),  # ← admin only
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user.is_active = False
    await db.flush()


# ── Promote to admin — Admin only ────────────────────────────
@router.patch(
    "/{user_id}/promote",
    response_model=UserResponse,
    summary="Promote user to admin  admin only",
)
async def promote_to_admin(
    user_id: int,
    db:      AsyncSession = Depends(get_db),
    admin:   User = Depends(get_current_admin),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    user.role = "admin"
    await db.flush()
    await db.refresh(user)
    return user
