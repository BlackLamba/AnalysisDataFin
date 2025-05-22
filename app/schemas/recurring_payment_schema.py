from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class RecurringPaymentCreate(BaseModel):
    user_id: int
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    name: str = Field(..., max_length=100)
    amount: float
    frequency: FrequencyEnum
    start_date: datetime
    end_date: Optional[datetime] = None


class RecurringPayment(RecurringPaymentCreate):
    payment_id: int

    model_config = ConfigDict(
        from_attributes=True
    )