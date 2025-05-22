from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BankAccountBase(BaseModel):
    account_number: str = Field(..., max_length=50, alias="AccountNumber")
    bank_name: Optional[str] = Field(None, max_length=100, alias="BankName")
    currency: str = Field(default="RUB", max_length=3, alias="Currency")
    is_active: bool = Field(default=True, alias="IsActive")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class BankAccountCreate(BankAccountBase):
    user_id: str = Field(..., alias="UserID")


class BankAccount(BankAccountBase):
    account_id: str = Field(..., alias="AccountID")
    balance: float = Field(..., alias="Balance")
    user_id: str = Field(..., alias="UserID")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )