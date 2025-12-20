from pydantic import BaseModel
from datetime import date

class MonthlySummaryResponse(BaseModel):
    year: int
    month: int
    total_amount: float

class CategorySummaryResponse(BaseModel):
    category_id: int
    total_amount: float

class CategorySummaryWithNameResponse(BaseModel):
    category_id: int
    category_name: str
    total_amount: float

class DailySummaryResponse(BaseModel):
    date: date
    total_amount: float