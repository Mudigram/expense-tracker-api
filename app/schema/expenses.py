from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from pydantic import ConfigDict

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str]
    created_at: datetime

class ExpenseOut(BaseModel):
    id: int
    amount: float
    description: str | None
    date: date
    category_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExpenseQuery(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)

class CategorySummary(BaseModel):
    category_id: int
    total_amount: float

class DailySummary(BaseModel):
    date: date
    total_amount: float

class MonthlySummary(BaseModel):
    month: str  # e.g. "2025-02"
    total_amount: float