from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import cast
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_sub = payload.get("sub")
        if token_sub is None:
            raise HTTPException(status_code=401, detail="Token missing subject (sub)")
        
        # This will fail if sub is "testuser10" instead of "10"
        user_id = int(token_sub) 
        
    except (JWTError, ValueError) as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User in token no longer exists")

    return user
