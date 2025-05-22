from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    amount: float
    description: Optional[str] = Field(None, max_length=255)
    transaction_date: Optional[datetime] = None  # можно не передавать


class Transaction(TransactionCreate):
    transaction_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )