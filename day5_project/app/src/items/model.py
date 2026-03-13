from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from database.base import Base


class Item(Base):
    __tablename__ = "items"

    id:         Mapped[int]                = mapped_column(Integer, primary_key=True, index=True)
    name:       Mapped[str]                = mapped_column(String(100), nullable=False)
    price:      Mapped[float]              = mapped_column(Float, nullable=False)
    owner_id:   Mapped[int]                = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime]           = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r} owner_id={self.owner_id}>"


class ItemCreate(BaseModel):
    name:  str   = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)


class ItemUpdate(BaseModel):
    name:  Optional[str]   = Field(None, min_length=2)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(BaseModel):
    id:         int
    name:       str
    price:      float
    owner_id:   int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
