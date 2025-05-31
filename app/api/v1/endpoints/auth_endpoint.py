from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LoginRequest
from app.schemas.token import TokenResponse
from app.services.auth_service import AuthService
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.login(
        email=login_data.email,
        password=login_data.password.get_secret_value() # <--- Получаем значение из SecretStr
    )