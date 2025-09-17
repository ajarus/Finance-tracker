# app/api/endpoints/transactions.py
from fastapi import APIRouter, Depends, HTTPException, status  # Добавляем status
from typing import List
from sqlalchemy.orm import Session  # Добавляем импорт Session

from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.services.transaction_service import TransactionService
from app.db.session import get_db  # Импортируем get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    from app.repositories.transaction_repository import TransactionRepositorySQLAlchemy
    repository = TransactionRepositorySQLAlchemy(db)
    return TransactionService(repository)

@router.get("/", response_model=List[Transaction])
async def get_user_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    """
    Получить список транзакций текущего пользователя с пагинацией.
    """
    try:
        transactions = service.get_user_transactions(
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Теперь status определен
            detail="Internal server error"
        )

# Остальные endpoint'ы остаются такими же, но с правильными импортами
@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    """
    Создать новую транзакцию.
    """
    try:
        transaction = service.create_transaction(
            transaction_data=transaction_data,
            user_id=current_user.id
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# ... остальные методы