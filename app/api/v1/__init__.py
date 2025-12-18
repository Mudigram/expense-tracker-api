# app/api/v1/__init__.py
from app.api.auth import router as auth_router
from app.api.expenses import router as expenses_router

__all__ = ["auth_router", "expenses_router"]