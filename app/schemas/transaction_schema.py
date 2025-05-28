from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class TransactionCreate(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")
    category_id: UUID4 = Field(..., alias="CategoryID")
    amount: float = Field(..., alias="Amount")
    account_id: UUID4 = Field(..., alias="AccountID")
    description: Optional[str] = Field(None, max_length=255, alias="Description")
    transaction_date: Optional[datetime] = Field(None, alias="TransactionDate")  # можно не передавать


class Transaction(TransactionCreate):
    transaction_id: UUID4 = Field(..., alias="TransactionID")

    model_config = ConfigDict(
        from_attributes=True
    )


class TransactionUpdate:
    pass


class TransactionStatsByPeriod(BaseModel):
    total_amount: float = Field(..., alias="total_amount")
    count: int = Field(..., alias="count")

    model_config = ConfigDict(
        from_attributes=True
    )


class TransactionStatsByCategory(BaseModel):
    category_name: str = Field(..., alias="category_name")
    total_amount: float = Field(..., alias="total_amount")
    count: int = Field(..., alias="count")

    model_config = ConfigDict(
        from_attributes=True
    )