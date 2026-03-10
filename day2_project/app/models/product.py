from pydantic import BaseModel, Field, computed_field
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    name:         str   = Field(..., min_length=2, max_length=100)
    sku:          str   = Field(..., description="e.g. SHOE-RED-42")
    price:        float = Field(..., gt=0, description="Must be > 0")  # ← BUG FIX
    stock:        int   = Field(..., ge=0)
    description:  Optional[str] = Field(None, max_length=500)
    tags:         List[str]     = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name:         Optional[str]   = Field(None, min_length=2, max_length=100)
    price:        Optional[float] = Field(None, gt=0)
    stock:        Optional[int]   = Field(None, ge=0)
    description:  Optional[str]   = None
    tags:         Optional[List[str]] = None


class ProductResponse(BaseModel):
    id:           int
    name:         str
    sku:          str
    price:        float
    stock:        int
    description:  Optional[str] = None
    tags:         List[str]     = []
    created_at:   datetime

    @computed_field
    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    model_config = {"from_attributes": True}
