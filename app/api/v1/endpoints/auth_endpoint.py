from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token import TokenResponse
from app.services.auth_service import AuthService
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.login(
        email=form_data.username,
        password=form_data.password
    )