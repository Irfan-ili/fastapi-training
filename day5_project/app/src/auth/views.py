from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.session  import get_db
from core.security     import hash_password, verify_password, create_access_token
from src.users.model   import User, UserCreate, UserResponse
from src.auth.model    import TokenResponse
from dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# ── HANDS-ON: Signup ──────────────────────────────────────────
@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
async def signup(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # Check if username or email already exists
    existing = await db.execute(
        select(User).where(
            (User.username == body.username) | (User.email == body.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    # Hash the password — NEVER save plain text!
    hashed = hash_password(body.password)

    # Create user in DB
    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hashed,
        role="user",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


# ── HANDS-ON: Login ───────────────────────────────────────────
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and receive JWT token",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    # Step 3 — create JWT token
    token = create_access_token(data={
        "sub":  user.username,
        "role": user.role,
    })

    # Step 4 — return token
    return TokenResponse(access_token=token, token_type="bearer")


# ── Get current user profile ──────────────────────────────────
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get my profile   requires login",
)
async def get_me(
    current_user: User = Depends(get_current_user),  # ← protected!
):

    return current_user
