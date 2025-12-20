from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.expenses import Expense
from app.schema.expenses import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate, DailySummary, CategorySummary
)
from app.utils.pagination import PaginatedResponse
from app.utils.pagination import PaginatedResponse
from app.services.expense_services import get_expenses
from app.services.summary import (
    get_category_summary,
    get_daily_summary,
    get_monthly_summary
)


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_expense = Expense(**expense.model_dump(), owner_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("", response_model=PaginatedResponse[ExpenseResponse])
def list_expenses(
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Expense).filter(Expense.owner_id == current_user.id)
    total = query.count()
    items = query.limit(limit).offset(offset).all()
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.owner_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.owner_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in expense_data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.owner_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()

@router.get("/summary/monthly", response_model=float)
def monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_monthly_summary(db, current_user.id, year, month)

@router.get("/summary/daily", response_model=list[DailySummary])
def daily_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_daily_summary(db, current_user.id)

@router.get("/summary/categories", response_model=list[CategorySummary])
def category_summary(db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    return get_category_summary(db, current_user.id)
