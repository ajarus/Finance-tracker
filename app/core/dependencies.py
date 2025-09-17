# app/core/dependencies.py
from typing import Generator, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import oauth2_scheme
from app.models.user import User
from app.services.user_service import UserService

def get_db() -> Generator:
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Зависимость для получения текущего аутентифицированного пользователя"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Зависимость для проверки активного пользователя"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Зависимости для сервисов
def get_user_service(db: Session = Depends(get_db)):
    from app.repositories.user_repository import UserRepositorySQLAlchemy
    repository = UserRepositorySQLAlchemy(db)
    return UserService(repository)

def get_transaction_service(db: Session = Depends(get_db)):
    from app.repositories.transaction_repository import TransactionRepositorySQLAlchemy
    repository = TransactionRepositorySQLAlchemy(db)
    from app.services.transaction_service import TransactionService
    return TransactionService(repository)

def get_analytics_service(db: Session = Depends(get_db)):
    from app.repositories.transaction_repository import TransactionRepositorySQLAlchemy
    repository = TransactionRepositorySQLAlchemy(db)
    from app.services.analytics_service import AnalyticsService
    return AnalyticsService(repository)