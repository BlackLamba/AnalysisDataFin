from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    verify_password,
    decode_token
)
from app.schemas.token import TokenResponse, TokenData
from app.services.user_service import UserService
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_email(self.db, email=email)  # Передаем db
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.authenticate_user(email=email, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = create_access_token(
            data={"sub": user.Email, "user_id": str(user.UserID)},
            expires_delta=timedelta(minutes=30)
        )
        return TokenResponse(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decode_token(
                token=token,
                secret_key=self.secret_key,
                algorithm=self.algorithm
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        user = await self.user_repository.get_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    async def refresh_token(self, token: str) -> TokenResponse:
        user = await self.get_current_user(token)
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.Email, "user_id": str(user.UserID)},
            expires_delta=access_token_expires,
            secret_key=self.secret_key,
            algorithm=self.algorithm
        )
        return TokenResponse(access_token=access_token, token_type="bearer")