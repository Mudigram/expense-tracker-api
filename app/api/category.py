from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schema.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut
)
from app.services.category_service import (
    get_categories,
    create_category,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_categories(db, current_user)

@router.post(
    "",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED
)
def create_new_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_category(db, category_in, current_user)

@router.put("/{category_id}", response_model=CategoryOut)
def update_existing_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_category(db, category_id, category_in, current_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this category"
        )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_category(db, category_id, current_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this category"
        )
