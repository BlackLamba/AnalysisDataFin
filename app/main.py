from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router
from app.core.database import engine, Base
import logging

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    # Создание экземпляра FastAPI с метаданными
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="API для учета личных финансов",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение роутеров
    app.include_router(
        api_router,
        prefix=settings.API_PREFIX
    )

    # События жизненного цикла
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up...")
        # Создание таблиц (только для разработки!)
        if settings.DEBUG:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down...")
        await engine.dispose()
        logger.info("Database connections closed")

    return app

# Создание экземпляра приложения
app = create_application()

# Для удобства тестирования
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)