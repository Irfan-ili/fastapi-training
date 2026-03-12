from sqlalchemy import column, Integer, String, Float, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

from database.base import Base


# ── ORM Model ─────────────────────────────────────────────────

class Product(Base):
    """Maps to the 'products' table in PostgreSQL."""
    __tablename__ = "products"

    id:          Mapped[int]                = mapped_column(Integer, primary_key=True, index=True)
    name:        Mapped[str]                = mapped_column(String(100), nullable=False)
    sku:         Mapped[str]                = mapped_column(String(50), unique=True, index=True)
    price:       Mapped[float]              = mapped_column(Float, nullable=False)
    stock:       Mapped[int]                = mapped_column(Integer, default=0)
    description: Mapped[Optional[str]]      = mapped_column(Text, nullable=True)
    created_at:  Mapped[datetime]           = mapped_column(DateTime, server_default=func.now())
    updated_at:  Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Product id={self.id} sku={self.sku!r} price={self.price}>"


# ── Pydantic Schemas ──────────────────────────────────────────

class ProductCreate(BaseModel):
    name:        str   = Field(..., min_length=2, max_length=100)
    sku:         str   = Field(..., description="e.g. LAPTOP-BLK-15")
    price:       float = Field(..., gt=0)
    stock:       int   = Field(0, ge=0)
    description: Optional[str] = None

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v):
        return v.upper()


class ProductUpdate(BaseModel):
    name:        Optional[str]   = Field(None, min_length=2)
    price:       Optional[float] = Field(None, gt=0)
    stock:       Optional[int]   = Field(None, ge=0)
    description: Optional[str]   = None


class ProductResponse(BaseModel):
    id:          int
    name:        str
    sku:         str
    price:       float
    stock:       int
    description: Optional[str] = None
    created_at:  datetime
    updated_at:  Optional[datetime] = None

    model_config = {"from_attributes": True}
