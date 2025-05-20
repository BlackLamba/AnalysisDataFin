from fastapi import APIRouter
from app.api.v1 import router as v1_router

# Создаем главный роутер API
api_router = APIRouter()

# Подключаем все версии API
api_router.include_router(v1_router, prefix="/v1")

# Можно добавить health-check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "ok"}