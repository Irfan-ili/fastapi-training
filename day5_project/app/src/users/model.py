from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from database.base import Base

# ── ORM Model ─────────────────────────────────────────────────

class User(Base):

    __tablename__ = "users"

    id:              Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    username:        Mapped[str]           = mapped_column(String(50), unique=True, index=True, nullable=False)
    email:           Mapped[str]           = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str]           = mapped_column(String(255), nullable=False)
    role:            Mapped[str]           = mapped_column(String(20), default="user")   # "user" or "admin"
    is_active:       Mapped[bool]          = mapped_column(Boolean, default=True)
    created_at:      Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())
    updated_at:      Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r} role={self.role!r}>"


# ── Pydantic Schemas ──────────────────────────────────────────

class UserCreate(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)
    email:    str = Field(..., description="Valid email")
    password: str = Field(..., min_length=6, description="Min 6 characters")


class UserResponse(BaseModel):

    id:         int
    username:   str
    email:      str
    role:       str
    is_active:  bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):

    username:  Optional[str] = Field(None, min_length=3)
    email:     Optional[str] = None
    is_active: Optional[bool] = None
