from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn
from typing import List, Optional
import secrets
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "Finance Tracker API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Настройки безопасности
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    ALGORITHM: str = "HS256"

    # Настройки базы данных
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    # CORS настройки
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Настройки логирования
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

    def configure_logging(self):
        logging.basicConfig(
            level=self.LOG_LEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger.info("Logging configured")

    @property
    def async_database_url(self) -> str:
        """Генерация DSN для asyncpg"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )


# Инициализация настроек
settings = Settings()
settings.configure_logging()

# Автоматически генерируем DATABASE_URL если он не указан
if not settings.DATABASE_URL:
    settings.DATABASE_URL = PostgresDsn.build(
        scheme="postgresql",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        path=f"/{settings.POSTGRES_DB}",
    )

logger.info(f"Loaded settings for {settings.PROJECT_NAME}")