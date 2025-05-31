from pydantic import BaseModel, EmailStr, Field, ConfigDict, SecretStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    last_name: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    passport_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    password: SecretStr = Field(..., min_length=8)  # Принимаем обычный пароль

class User(BaseModel):
    user_id: UUID = Field(alias="UserID")  # Если в модели User.UserID
    last_name: str = Field(alias="LastName")  # Если в модели User.LastName
    first_name: str = Field(alias="FirstName")
    middle_name: str | None = Field(default=None, alias="MiddleName")
    passport_number: str = Field(alias="PassportNumber")
    email: EmailStr = Field(alias="Email")
    registration_date: datetime = Field(alias="RegistrationDate")

    model_config = ConfigDict(
        from_attributes=True
    )

class UserUpdate(BaseModel):
    last_name: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    password: Optional[SecretStr] = Field(None, min_length=8)