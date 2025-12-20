from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User

from app.services.summary import (
    get_monthly_summary,
    get_category_summary,
    get_daily_summary
)

from app.schema.summary import (
    MonthlySummaryResponse,
    CategorySummaryResponse,
    DailySummaryResponse
)

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

@router.get(
    "/monthly",
    response_model=MonthlySummaryResponse
)
def monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MonthlySummaryResponse:
    total = get_monthly_summary(
        db=db,
        user_id= int(current_user.id),
        year=year,
        month=month
    )

    return MonthlySummaryResponse(
        year=year,
        month=month,
        total_amount=total
    )

@router.get(
    "/by-category",
    response_model=list[CategorySummaryResponse]
)
def category_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[CategorySummaryResponse]:
    results = get_category_summary(
        db=db,
        user_id=current_user.id
    )

    return [
        CategorySummaryResponse(
            category_id=row["category_id"],
            total_amount=row["total_amount"]
        )
        for row in results
    ]

@router.get(
    "/daily",
    response_model=list[DailySummaryResponse]
)
def daily_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[DailySummaryResponse]:
    results = get_daily_summary(
        db=db,
        user_id=int(current_user.id)
    )

    return [
        DailySummaryResponse(
            date=row["date"],
            total_amount=row["total_amount"]
        )
        for row in results
    ]
