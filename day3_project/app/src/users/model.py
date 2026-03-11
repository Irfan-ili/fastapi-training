from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email:    str = Field(..., description="User email address")


class UserResponse(BaseModel):
    id:         int
    username:   str
    email:      str
    created_at: str
