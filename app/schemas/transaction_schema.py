from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.base_schema import BaseSchema, IDSchema

class TransactionBase(BaseSchema):
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=255)
    transaction_date: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(TransactionBase):
    user_id: str
    category_id: Optional[str] = None
    account_id: str

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[str] = None

class Transaction(IDSchema, TransactionBase):
    user_id: str
    category_id: Optional[str]
    account_id: str