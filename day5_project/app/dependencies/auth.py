from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.session   import get_db
from core.security      import decode_access_token
from src.users.model    import User
from src.auth.model     import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── TOPIC: Protected Routes ───────────────────────────────────

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db:    AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1 — decode the JWT token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Step 2 — extract username from payload
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Step 3 — load user from DB
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    # Step 4 — check user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return user


# ── TOPIC: Role-Based Access Control ─────────────────────────

async def get_current_admin(
    current_user: User = Depends(get_current_user),  # ← nested dependency
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
