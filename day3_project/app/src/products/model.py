from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProductCreate(BaseModel):
    name:        str   = Field(..., min_length=2, max_length=100)
    sku:         str   = Field(..., description="e.g. LAPTOP-BLK-15")
    price:       float = Field(..., gt=0)
    stock:       int   = Field(..., ge=0)
    description: Optional[str] = None

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v):
        return v.upper()


class ProductUpdate(BaseModel):
    name:        Optional[str]   = None
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
    created_at:  str
