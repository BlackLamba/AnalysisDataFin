# app/core/config.py
from pydantic import BaseModel, field_validator, AnyHttpUrl
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings # Убедитесь, что импорт правильный

from typing import List, Optional, Union
import secrets
import logging
from pathlib import Path
import json # Добавлен для parse_cors_origins

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "Finance Tracker API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    API_PREFIX: str = "/api/v1"

    # Настройки безопасности
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"

    # Настройки базы данных
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432  # <--- ВОТ ЭТО ПОЛЕ НУЖНО ДОБАВИТЬ
                                # Укажите значение по умолчанию, если хотите
    DATABASE_URL: Optional[str] = None
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # CORS настройки
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_SERVER")
        port = info.data.get("POSTGRES_PORT")  # Теперь это поле существует
        db = info.data.get("POSTGRES_DB")

        # Простая сборка URL с портом
        # Если POSTGRES_SERVER уже содержит порт (например, "localhost:5000"),
        # то эта логика может потребовать уточнения, чтобы не дублировать порт.
        # Для простоты предполагаем, что POSTGRES_SERVER - это только хост.
        if port:
             return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        return f"postgresql+asyncpg://{user}:{password}@{host}/{db}" # Если порт не указан или стандартный

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse BACKEND_CORS_ORIGINS JSON string: {v}. Falling back to comma-separated.")
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return [str(origin) for origin in v]
        return v # Добавлено для корректной обработки, если v уже List[AnyHttpUrl]
                 # или если это не строка и не список (хотя Pydantic должен это обработать)

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        v = v.upper()
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log level")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        # extra = "ignore" # Можно явно добавить, если проблема останется,
                           # хотя для BaseSettings это дефолт

    def configure_logging(self) -> None:
        """Настройка логгирования для приложения"""
        # ... (остальной код configure_logging без изменений) ...
        config = {
            "level": self.LOG_LEVEL,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "handlers": [logging.StreamHandler()]
        }

        if self.LOG_FILE:
            Path(self.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
            config["handlers"].append(logging.FileHandler(self.LOG_FILE))

        logging.basicConfig(**config)
        logger.info("Logging configured for %s environment", self.ENVIRONMENT)


# Инициализация настроек
settings = Settings()
settings.configure_logging()

# Логирование важных настроек (без паролей)
logger.info("Application initialized in %s mode", "DEBUG" if settings.DEBUG else "PRODUCTION")
logger.info("Database host: %s, port: %s", settings.POSTGRES_SERVER, settings.POSTGRES_PORT) # Добавил порт в лог
logger.info("Database URL: %s", settings.DATABASE_URL) # Логируем собранный URL для проверки
logger.info("CORS allowed origins: %s", settings.BACKEND_CORS_ORIGINS)