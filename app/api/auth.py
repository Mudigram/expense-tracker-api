from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import cast
from app.schema.user import UserCreate, UserLogin, Token
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        or_(
            User.email == user_in.email,
            User.username == user_in.username
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


@router.post("/login", response_model=Token)
async def login(request: Request, db: Session = Depends(get_db)):
    """Accept either form data (for Swagger "Authorize" or tests) or JSON body.

    JSON format: {"identifier": "<username-or-email>", "password": "..."}
    Form format: username=<username-or-email>&password=<password> or identifier=<...>&password=<...>
    """
    ctype = request.headers.get("content-type", "")
    identifier = None
    password = None

    if ctype.startswith("application/json"):
        body = await request.json()
        identifier = body.get("identifier")
        password = body.get("password")
    else:
        form = await request.form()
        # support both `username` (OAuth standard) and `identifier` (tests)
        identifier = form.get("identifier") or form.get("username")
        password = form.get("password")

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    user = db.query(User).filter(
        or_(User.email == identifier, User.username == identifier)
    ).first()

    if not user or not verify_password(cast(str, password), cast(str, user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
