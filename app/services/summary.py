from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from app.models.expenses import Expense
from app.models.category import Category

def get_monthly_summary(
    db: Session,
    user_id: int,
    year: int,
    month: int
) -> float:
    total = db.query(
        func.coalesce(func.sum(Expense.amount), 0.0)
    ).filter(
        Expense.owner_id == user_id,
        extract("year", Expense.created_at) == year,
        extract("month", Expense.created_at) == month
    ).scalar()

    return float(total)

def get_category_summary(
    db: Session,
    user_id: int
) -> list[dict]:
    rows = (
        db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.coalesce(func.sum(Expense.amount), 0.0).label("total_amount")
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(
            Expense.owner_id == user_id
        )
        .group_by(
            Category.id,
            Category.name
        )
        .all()
    )

    return [
        {
            "category_id": r.category_id,
            "category_name": r.category_name,
            "total_amount": float(r.total_amount),
        }
        for r in rows
    ]

def get_daily_summary(
    db,
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None
):
    query = db.query(
        Expense.date,
        func.sum(Expense.amount).label("total_amount")
    ).filter(
        Expense.user_id == user_id
    )

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.group_by(
        Expense.date
    ).order_by(
        Expense.date
    ).all()
