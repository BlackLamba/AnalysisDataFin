from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TokenType(str, Enum):
    """Типы токенов"""
    BEARER = "bearer"
    REFRESH = "refresh"

class TokenBase(BaseModel):
    """Базовая схема токена"""
    token_type: TokenType = Field(default=TokenType.BEARER, description="Тип токена")
    expires_at: Optional[datetime] = Field(None, description="Время истечения срока действия")

class TokenCreate(TokenBase):
    """Схема для создания токена"""
    user_id: str = Field(..., description="ID пользователя")
    email: str = Field(..., description="Email пользователя")

class TokenPayload(BaseModel):
    """Схема данных в payload токена"""
    sub: str = Field(..., description="Subject (обычно email пользователя)")
    user_id: str = Field(..., description="ID пользователя")
    exp: int = Field(..., description="Время истечения в timestamp")

class TokenResponse(TokenBase):
    """Схема ответа с токеном"""
    access_token: str = Field(..., description="JWT токен доступа")
    refresh_token: Optional[str] = Field(None, description="Токен для обновления")

class RefreshTokenRequest(BaseModel):
    """Схема запроса на обновление токена"""
    refresh_token: str = Field(..., description="Refresh токен")

class TokenData(BaseModel):
    """Схема данных из токена"""
    email: Optional[str] = Field(None, description="Email пользователя")
    user_id: Optional[str] = Field(None, description="ID пользователя")

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }

__all__ = [
    "TokenType",
    "TokenBase",
    "TokenCreate",
    "TokenPayload",
    "TokenResponse",
    "RefreshTokenRequest",
    "TokenData"
]