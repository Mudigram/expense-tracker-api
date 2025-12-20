# app/api/v1/__init__.py
from app.api.auth import router as auth_router
from app.api.expenses import router as expenses_router
from app.api.category import router as category_router
from app.api.summary import router as summary_router
from app.api.dashboard import router as dashboard_router

__all__ = ["auth_router", "expenses_router", "summary_router", "category_router", "dashboard_router"]