from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from database.base import Base

# ── PART 1: ORM Model (SQLAlchemy) ───────────────────────────

class Item(Base):
    __tablename__ = "items"

    # mapped_column = modern SQLAlchemy 2.x style (type-safe)
    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    name:       Mapped[str]           = mapped_column(String(100), nullable=False)
    price:      Mapped[float]         = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r} price={self.price}>"


# ── PART 2: Pydantic Schemas ──────────────────────────────────

class ItemCreate(BaseModel):
    """Schema for POST /items — what client sends."""
    name:  str   = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0, description="Must be > 0")


class ItemUpdate(BaseModel):
    """Schema for PATCH /items/{id} — all fields optional."""
    name:  Optional[str]   = Field(None, min_length=2, max_length=100)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(BaseModel):
    """Schema for responses — what client receives."""
    id:         int
    name:       str
    price:      float
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Allows Pydantic to read from SQLAlchemy ORM objects, Required when returning ORM models.
    model_config = {"from_attributes": True}
