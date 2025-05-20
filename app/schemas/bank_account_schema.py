from typing import Optional

from pydantic import BaseModel, Field
from app.schemas.base_schema import BaseSchema, IDSchema

class BankAccountBase(BaseSchema):
    account_number: str = Field(..., max_length=50)
    bank_name: Optional[str] = Field(None, max_length=100)
    currency: str = Field(default="RUB", max_length=3)
    is_active: bool = Field(default=True)

class BankAccountCreate(BankAccountBase):
    user_id: str

class BankAccountUpdate(BaseModel):
    bank_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class BankAccount(IDSchema, BankAccountBase):
    balance: float
    user_id: str