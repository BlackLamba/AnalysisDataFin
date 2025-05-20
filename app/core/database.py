# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Асинхронный движок БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логировать SQL-запросы в debug-режиме
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True
)

# Фабрика сессий для работы с БД
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """
    Генератор сессий для dependency injection.
    Использование:
    async with get_db() as db:
        await db.execute(...)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()

async def init_db():
    """
    Инициализация БД (создание таблиц).
    Используется только при первом запуске/тестировании.
    В продакшене используйте миграции Alembic.
    """
    async with engine.begin() as conn:
        if settings.DEBUG:
            logger.info("Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully")

async def close_db():
    """Корректное закрытие соединений с БД"""
    await engine.dispose()
    logger.info("Database connections closed")

# Для удобного импорта
__all__ = ["Base", "engine", "AsyncSessionLocal", "get_db", "init_db", "close_db"]