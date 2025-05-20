from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.base_schema import BaseSchema, IDSchema
from datetime import datetime
from uuid import UUID

class UserBase(BaseSchema):
    email: EmailStr
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    passport_number: Optional[str] = Field(None, max_length=20)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=64)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=64)

class UserInDB(IDSchema, UserBase):
    registration_date: datetime
    is_active: bool

    # Добавляем конфигурацию для ORM mode (ранее назывался orm_mode)
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# Новые схемы для аутентификации
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID] = None