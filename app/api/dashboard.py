from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schema.dashboard import DashboardResponse, CategorySummary, DailySummary
from app.services.summary import (
    get_monthly_summary,
    get_category_summary,
    get_daily_summary
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    monthly_total = get_monthly_summary(
        db=db,
        user_id=current_user.id,
        year=year,
        month=month
    )

    categories = get_category_summary(
        db=db,
        user_id=current_user.id
    )

    daily = get_daily_summary(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return DashboardResponse(
        year=year,
        month=month,
        monthly_total=monthly_total,
        by_category=[
            CategorySummary(
                category_id=row["category_id"],
                category_name=row["category_name"],
                total_amount=row["total_amount"]
            )
            for row in categories
        ],
        daily=[
            DailySummary(
                date=row["date"],
                total_amount=row["total_amount"]
            )
            for row in daily
        ]
    )
