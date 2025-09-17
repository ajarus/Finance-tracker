# app/api/endpoints/analytics.py
from fastapi import APIRouter, Depends, HTTPException, status  # Добавляем status
from datetime import date
from typing import Dict, Any
from sqlalchemy.orm import Session  # Добавляем импорт Session

from app.services.analytics_service import AnalyticsService
from app.db.session import get_db  # Импортируем get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    from app.repositories.transaction_repository import TransactionRepositorySQLAlchemy
    repository = TransactionRepositorySQLAlchemy(db)
    return AnalyticsService(repository)

@router.get("/summary")
async def get_financial_summary(
    start_date: date,
    end_date: date,
    current_user: User = Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service)
) -> Dict[str, Any]:
    """
    Получить финансовую сводку за период.
    """
    try:
        summary = service.get_financial_summary(
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Теперь status определен
            detail="Error generating summary"
        )

@router.get("/categories")
async def get_category_analytics(
    start_date: date,
    end_date: date,
    current_user: User = Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service)
) -> Dict[str, float]:
    """
    Получить распределение расходов по категориям.
    """
    analytics = service.get_category_analytics(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    return analytics