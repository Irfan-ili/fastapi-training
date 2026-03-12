from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from database.base import Base


# ── ORM Model ─────────────────────────────────────────────────

class User(Base):
    """Maps to the 'users' table in PostgreSQL."""
    __tablename__ = "users"

    id:         Mapped[int]                = mapped_column(Integer, primary_key=True, index=True)
    username:   Mapped[str]                = mapped_column(String(50), unique=True, index=True)
    email:      Mapped[str]                = mapped_column(String(100), unique=True, index=True)
    is_active:  Mapped[bool]               = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]           = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"


# ── Pydantic Schemas ──────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email:    str = Field(..., description="Valid email address")


class UserUpdate(BaseModel):
    username:  Optional[str]  = Field(None, min_length=3, max_length=50)
    email:     Optional[str]  = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id:         int
    username:   str
    email:      str
    is_active:  bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
