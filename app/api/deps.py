from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core import security
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/api/auth/token") # path used for login


def get_db():
    
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(
            token, 
            security.SECRET_KEY,
            algorithms=[security.ALGORITHM]
        )
        user_id : int =  payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authentcate" : "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authentcate" : "Bearer"},
        )
    # Fetch user from db
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_admin_user(current_user: User = Depends(get_current_user)):

    if not current_user.is_admin:  # <-- use is_admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
    