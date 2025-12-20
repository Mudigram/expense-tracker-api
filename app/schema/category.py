from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from pydantic import ConfigDict

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

class CategoryOut(CategoryBase):
    id: int
    owner_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
