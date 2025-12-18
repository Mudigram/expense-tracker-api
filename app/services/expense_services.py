from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.expenses import Expense
from app.schema.expenses import ExpenseQuery

def get_expenses(
    db: Session,
    user_id: int,
    query: ExpenseQuery,
    limit: int,
    offset: int
):
    stmt = select(Expense).where(Expense.user_id == user_id)

    if query.start_date:
        stmt = stmt.where(Expense.date >= query.start_date)

    if query.end_date:
        stmt = stmt.where(Expense.date <= query.end_date)

    if query.category_id:
        stmt = stmt.where(Expense.category_id == query.category_id)

    if query.min_amount is not None:
        stmt = stmt.where(Expense.amount >= query.min_amount)

    if query.max_amount is not None:
        stmt = stmt.where(Expense.amount <= query.max_amount)

    total = db.scalar(
        select(func.count()).select_from(stmt.subquery())
    )

    items = db.scalars(
        stmt.limit(limit).offset(offset)
    ).all()

    return items, total
