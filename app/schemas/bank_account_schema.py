from pydantic import BaseModel, Field, UUID4
from uuid import UUID
from typing import Optional
from datetime import datetime

class BankAccountBase(BaseModel):
    account_number: str = Field(..., max_length=50, alias="AccountNumber")
    bank_name: Optional[str] = Field(None, max_length=100, alias="BankName")
    currency: str = Field(default="RUB", max_length=3, alias="Currency")
    is_active: bool = Field(default=True, alias="IsActive")

class BankAccountCreate(BankAccountBase):
    user_id: UUID4 = Field(..., alias="UserID")  # Используем UUID4 тип

class BankAccount(BankAccountBase):
    account_id: UUID4 = Field(..., alias="AccountID")  # UUID4 вместо str
    user_id: UUID4 = Field(..., alias="UserID")
    balance: float = Field(..., alias="Balance")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            UUID: lambda v: str(v)  # Автоматическое преобразование в строку при сериализации
        }


class BankAccountUpdate:
    pass