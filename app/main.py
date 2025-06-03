from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

from app.core.config import settings
from app.api import api_router
from app.core.database import engine, Base, init_db, close_db
import logging
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import models

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

    # Путь до клиентской папки
    client_path = Path(__file__).resolve().parent / "client"
    app.mount("/static", StaticFiles(directory=client_path, html=False), name="static")
    @app.get("/")
    async def serve_index():
        return FileResponse(client_path / "html" / "index.html")

    @app.get("/login")
    async def serve_login():
        return FileResponse(client_path / "html" / "login.html")

    @app.get("/register")
    async def serve_register():
        return FileResponse(client_path / "html" / "register.html")

    @app.get("/dashboard")
    async def serve_dashboard():
        return FileResponse(client_path / "html" / "dashboard.html")

    @app.get("/analytics")
    async def serve_analytics():
        return FileResponse(client_path / "html" / "analytics.html")

    @app.get("/input")
    async def serve_input():
        return FileResponse(client_path / "html" / "input.html")

    @app.get("/settings")
    async def serve_settings():
        return FileResponse(client_path / "html" / "settings.html")

    # События жизненного цикла
    @app.on_event("startup")
    async def on_startup():
        logger.info("Application startup...")
        # Для отладки можно вывести здесь
        logger.info(f"Tables known to Base before init_db: {Base.metadata.tables.keys()}")
        await init_db()
        logger.info(f"Tables known to Base after init_db: {Base.metadata.tables.keys()}")  # Должны появиться таблицы
        logger.info("Database initialized.")

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