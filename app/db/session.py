# app/db/session.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings

# Создание engine (движка БД)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20,        # Максимальный размер пула соединений
    max_overflow=10,     # Максимум дополнительных соединений
    echo=settings.DEBUG  # Логирование SQL запросов в debug mode
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,    # Автокоммит отключен
    autoflush=False,     # Автофлуш отключен
    bind=engine,
    expire_on_commit=False  # Объекты не expire после коммита
)

# Scoped session для thread-safe использования
SessionScoped = scoped_session(SessionLocal)

def get_db() -> Generator:
    """
    Зависимость для получения сессии БД.
    Используется в FastAPI Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Важно всегда закрывать сессию!

# Альтернативная версия для использования вне FastAPI
class DatabaseSessionManager:
    def __init__(self):
        self._engine = engine
        self._session_factory = SessionLocal

    def __enter__(self):
        self.session = self._session_factory()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

# Глобальный менеджер сессий
session_manager = DatabaseSessionManager()