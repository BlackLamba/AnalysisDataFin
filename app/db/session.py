from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import AsyncGenerator

# Создаем асинхронный движок для PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логировать SQL-запросы в debug-режиме
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True  # Проверять соединения перед использованием
)

# Фабрика сессий с настройками
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
Зависимость FastAPI для предоставления асинхронной сессии БД.
Используется как Depends(get_db) в эндпоинтах.
"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def close_db_connection():
    """Корректное закрытие соединений с БД при завершении приложения"""
    await engine.dispose()