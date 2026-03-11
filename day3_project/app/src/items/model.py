
from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name:  str   = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0, description="Must be greater than 0")


class ItemUpdate(BaseModel):
    name:  Optional[str]   = Field(None, min_length=2)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(BaseModel):
    id:         int
    name:       str
    price:      float
    created_at: str
