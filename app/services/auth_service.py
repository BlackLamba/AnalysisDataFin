from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash, decode_token
)
from app.schemas.token import TokenResponse, TokenData
from app.schemas.user_schema import UserLogin
from app.services.user_service import UserService
from app.models.user import User

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_service.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, user_login: UserLogin) -> TokenResponse:
        user = await self.authenticate_user(
            email=user_login.email,
            password=user_login.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires,
            secret_key=self.secret_key,
            algorithm=self.algorithm
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

        user = await self.user_service.get_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    async def refresh_token(self, token: str) -> TokenResponse:
        user = await self.get_current_user(token)
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires,
            secret_key=self.secret_key,
            algorithm=self.algorithm
        )
        return TokenResponse(access_token=access_token, token_type="bearer")