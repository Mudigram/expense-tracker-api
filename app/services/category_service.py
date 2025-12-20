from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.category import Category
from app.models.user import User
from app.schema.category import CategoryCreate, CategoryUpdate

def get_categories(db: Session, user: User) -> List[Category]:
    """
    Returns:
    - system categories (owner_id is NULL)
    - user-specific categories
    """
    return (
        db.query(Category)
        .filter(
            (Category.owner_id == None) | (Category.owner_id == user.id)
        )
        .order_by(Category.name.asc())
        .all()
    )

def create_category(
    db: Session,
    category_in: CategoryCreate,
    user: User
) -> Category:
    category = Category(
        name=category_in.name,
        owner_id=user.id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def update_category(
    db: Session,
    category_id: int,
    category_in: CategoryUpdate,
    user: User
) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise ValueError("Category not found")

    if category.owner_id != user.id: # type: ignore
        raise PermissionError("Not allowed to update this category")

    if category_in.name is not None:
        category.name = category_in.name # type: ignore

    db.commit()
    db.refresh(category)

    return category

def delete_category(
    db: Session,
    category_id: int,
    user: User
) -> None:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise ValueError("Category not found")

    if category.owner_id != user.id: # type: ignore
        raise PermissionError("Not allowed to delete this category")

    db.delete(category)
    db.commit()
