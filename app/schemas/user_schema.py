from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    last_name: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    passport_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    hashed_password: str = Field(..., max_length=255)  # ⚠️ В идеале — хешируй до создания


class User(BaseModel):
    user_id: UUID
    last_name: str
    first_name: str
    middle_name: Optional[str]
    passport_number: Optional[str]
    email: EmailStr
    registration_date: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True
    )