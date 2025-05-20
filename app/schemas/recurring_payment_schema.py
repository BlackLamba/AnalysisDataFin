from typing import Optional

from pydantic import BaseModel, Field
from datetime import date
from app.schemas.base_schema import BaseSchema, IDSchema

class RecurringPaymentBase(BaseSchema):
    name: str = Field(..., max_length=100)
    amount: float = Field(..., gt=0)
    frequency: str = Field(..., regex="^(daily|weekly|monthly|yearly)$")
    start_date: date
    end_date: Optional[date] = None

class RecurringPaymentCreate(RecurringPaymentBase):
    user_id: str
    category_id: Optional[str] = None
    account_id: Optional[str] = None

class RecurringPaymentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    frequency: Optional[str] = Field(None, regex="^(daily|weekly|monthly|yearly)$")
    end_date: Optional[date] = None

class RecurringPayment(IDSchema, RecurringPaymentBase):
    user_id: str
    category_id: Optional[str]
    account_id: Optional[str]